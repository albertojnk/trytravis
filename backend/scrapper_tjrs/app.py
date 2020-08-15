import asyncio
import json
import traceback
from typing import List

import pandas as pd
import sqlalchemy as sa
from fastapi import (Depends, FastAPI, File, HTTPException, UploadFile,
                     WebSocket, WebSocketDisconnect)
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from tqdm import tqdm

from .captcha import CaptchaSolver
from .model import Base, PydanticProcess, SessionLocal
from .tjrs import TJRS

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>

        <input id="file" type="file">
        <input type="button" value="Upload" onclick="sendFile()" />

        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);

            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendFile() {

                var file = document.getElementById('file').files[0];

                var reader = new FileReader();

                var rawData = new ArrayBuffer();

                reader.onload = function(e) {

                    var rawData = e.target.result;
                    var byteArray = new Uint8Array(rawData);
                    var fileByteArray = [];
                    ws.send(byteArray.buffer);
                };
                reader.readAsArrayBuffer(file);

            }
        </script>
    </body>
</html>
"""

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.websocket('/ws/{client_id}')
async def websocket_ep(websocket: WebSocket, client_id: int, db: Session = Depends(get_db)):
    await websocket.accept()

    while True:
        data = await websocket.receive_bytes()
        df = pd.read_excel(data, sheet_name="1", converters={"processos": lambda x: str(x)})
        process_list = df.values.tolist()

        await websocket.send_text("hello from server")
        await asyncio.sleep(0)

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

                await websocket.send_json(PydanticProcess.from_orm(p).dict())
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

@app.get("/")
async def main():
    content = """
<body>
<form action="/do_magic/" enctype="multipart/form-data" method="post">
<input name="file" type="file">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

@app.get("/test")
async def ws_test():
    return HTMLResponse(content=html)


