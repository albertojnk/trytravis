
##################################################################################################
##################################################################################################
##################################################################################################
### SE ESTIVER DANDO ERRO DE SHAPE NA HORA DO load_model, MUDAR PARA 200 A LINHA 86 DO CAPTCHA ###
##################################################################################################
##################################################################################################
##################################################################################################


import numpy as np
from acessatjrs import AcessarSite
from captcha import CaptchaSolver
import pandas
from tqdm import tqdm
import unicodedata
import time


solver = CaptchaSolver()
site = AcessarSite()


perinni = pandas.read_excel("1.xlsx", sheet_name="1", converters={
                            'processos': lambda x: str(x)})
lista = perinni.values.tolist()

total = 0
errou = 0

debug = True

for codigoConsulta in tqdm(lista):
    for _ in range(10): # repetir varias vezes o acesso ao mesmo codigo caso a rede erre

        tempo = time.time()
        site.novo_acesso()
        if(debug):
            print('\nNOVO_ACESSO', time.time() - tempo)

        tempo = time.time()
        image = site.pegar_captcha()
        if(debug):
            print('\nPEGAR_CAPTCHA', time.time() - tempo)

        tempo = time.time()
        image = solver.preprocess_image(image)
        if(debug):
            print('\nPREPROCESS', time.time() - tempo)

        tempo = time.time()
        codigo = solver.predict(image)
        if(debug):
            print('\nPREDICT', time.time() - tempo)

        tempo = time.time()
        result = site.make_request(codigoConsulta, codigo, debug)
        if(debug):
            print('\nMAKE_REQUEST', time.time() - tempo)

        total +=1
        
        if("verificador" in result.url):
            errou += 1
        else:
            break

    tempo = time.time()
    site.get_data(result, codigoConsulta)
    if(debug):
        print('\nGET_DATA', time.time() - tempo,'\n\n')
    site.save_data()
    
print('CaptchaSolver errou: {}'.format(errou), 'captchas')
print('Total: {}'.format(total), 'captchas')
print('Porcentagem de acertos: {}%'.format((1-errou/total)*100))
