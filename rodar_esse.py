import os
import logging

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logging.getLogger("tensorflow").disabled = True
import numpy as np
from acessatjrs import AcessarSite
from captcha import CaptchaSolver
import pandas
from tqdm import tqdm
import unicodedata
import time
import sys


solver = CaptchaSolver()
site = AcessarSite()


perinni = pandas.read_excel(
    "1.xlsx", sheet_name="1", converters={"processos": lambda x: str(x)}
)
lista = perinni.values.tolist()

checkstart = 0
if os.path.exists("checkpoint.txt"):
    with open("checkpoint.txt", "r") as check:
        checkstart = int(check.read())
        lista = lista[checkstart:]

total = 0
errou = 0

debug = False

for codigoConsulta, i in tqdm(zip(lista, range(len(lista))), total=len(lista)):
    try:
        for _ in range(
            10
        ):  # repetir varias vezes o acesso ao mesmo codigo caso a rede erre

            tempo = time.time()
            site.novo_acesso()
            if debug:
                print("\nNOVO_ACESSO", time.time() - tempo)

            tempo = time.time()
            image = site.pegar_captcha()
            if debug:
                print("PEGAR_CAPTCHA", time.time() - tempo)

            tempo = time.time()
            image = solver.preprocess_image(image)
            if debug:
                print("PREPROCESS", time.time() - tempo)

            tempo = time.time()
            codigo = solver.predict(image)
            if debug:
                print("PREDICT", time.time() - tempo)

            tempo = time.time()
            result = site.make_request(codigoConsulta, codigo, debug)
            if debug:
                print("MAKE_REQUEST", time.time() - tempo)

            total += 1

            if "verificador" in result.url:
                errou += 1
            else:
                break

        tempo = time.time()
        site.get_data(result, codigoConsulta)
        if debug:
            print("GET_DATA", time.time() - tempo, "\n\n")
        site.save_data()
    except Exception as e:
        print(e)
        with open("checkpoint.txt", "w") as check:
            check.write(str(i+checkstart))
        #os.system("python rodar_esse.py")
        sys.exit("batatinha")
    except KeyboardInterrupt:
        with open("checkpoint.txt", "w") as check:
            check.write(str(i+checkstart))
        sys.exit("perinni")

print("CaptchaSolver errou: {}".format(errou), "captchas")
print("Total: {}".format(total), "captchas")
print("Porcentagem de acertos: {}%".format((1 - errou / total) * 100))
if os.path.exists("checkpoint.txt"):
   os.remove("checkpoint.txt")
