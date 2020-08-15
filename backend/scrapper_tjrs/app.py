import asyncio
import json
import traceback
from typing import List

import pandas as pd
import sqlalchemy as sa
from fastapi import (Depends, FastAPI, File, HTTPException, UploadFile,
                     WebSocket, WebSocketDisconnect)
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from tqdm import tqdm

from .captcha import CaptchaSolver
from .model import Base, PydanticProcess, SessionLocal, Process
from .tjrs import TJRS

app = FastAPI()

origins = [
    "http://localhost:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.websocket('/ws')
async def websocket_ep(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()

    while True:
        data = await websocket.receive_bytes()
        df = pd.read_excel(data, sheet_name="1", converters={"processos": lambda x: str(x)})
        process_list = df.values.tolist()

        total = 0
        miss = 0
        solver = CaptchaSolver()
        tjrs = TJRS()

        for process_num, i in tqdm(zip(process_list, range(len(process_list))), total=len(process_list)):
            try:
                # try again if captcha fails
                for _ in range(10):

                    tjrs.new_access()

                    image = tjrs.get_captcha()

                    image = solver.preprocess_image(image)

                    captcha = solver.predict(image)

                    result = tjrs.make_request(process_num[0], captcha)
                    total += 1

                    if "verificador" in result.url:
                        miss += 1
                    else:
                        break

                p = tjrs.get_data(result, process_num[0])
                db.add(p)
                db.commit()
                response = PydanticProcess.from_orm(p).dict()
                response['progress'] = ((i + 1) /  len(process_list)) * 100
                await websocket.send_json(response)
                await asyncio.sleep(0)

            except Exception as e:
                traceback.print_exc()


@app.post("/do_magic")
async def do_magic(file: UploadFile = File(...), db: Session = Depends(get_db)):

    solver = CaptchaSolver()
    tjrs = TJRS()
    content = await file.read()
    df = pd.read_excel(content, sheet_name="1", converters={"processos": lambda x: str(x)})

    process_list = df.values.tolist()

    total = 0
    miss = 0

    for process_num, i in tqdm(zip(process_list, range(len(process_list))), total=len(process_list)):
        try:
            # try again if captcha fails
            for _ in range(10):

                tjrs.new_access()

                image = tjrs.get_captcha()

                image = solver.preprocess_image(image)

                captcha = solver.predict(image)

                result = tjrs.make_request(process_num[0], captcha)
                total += 1

                if "verificador" in result.url:
                    miss += 1
                else:
                    break

            p = tjrs.get_data(result, process_num[0])
            db.add(p)
            db.commit()

        except Exception as e:
            traceback.print_exc()

    return {"message": tjrs.time}

@app.get("/procedures/{created_id}")
async def do_something(created_id: str, db: Session = Depends(get_db)):
    result = db.query(Process).filter(Process.created == created_id).all()

    return dict(procedures = [PydanticProcess.from_orm(p).dict() for p in result ])