
from bs4 import BeautifulSoup
import requests
from requests import session
import cv2
from urllib.request import urlopen
import urllib
import re
from lxml import html, etree
import pandas
import numpy as np
from PIL import Image
import unicodedata
from datetime import datetime
from collections import defaultdict


dicionario_cnj = {"7000": "700", "0001": "porto_alegre", "5001": "porto_alegre", "2001": "porto_alegre", "6001": "porto_alegre", "4001": "porto_alegre", "9000": "710", "0002": "alegrete", "0003": "alvorada", "0004": "bage", "0005": "bento_goncalves", "0006": "cachoeira_sul", "0008": "canoas", "0009": "carazinho", "0010": "caxias_sul",   "0012": "dom_pedrito", "0014": "esteio", "0017": "lajeado", "0018": "montenegro", "0019": "novo_hamburgo", "0021": "passo_fundo", "0022": "pelotas", "0023": "rio_grande", "0024": "rio_pardo", "0025": "santana_livramento", "0026": "santa_cruz_sul", "0027": "santa_maria", "0028": "santa_rosa", "0029": "santo_angelo", "0030": "sao_borja", "0033": "sao_leopoldo", "0034": "sao_luis_gonzaga", "0036": "soledade", "0037": "uruguaiana", "0038": "vacaria", "0039": "viamao", "0042": "cangucu", "0046": "espumoso", "0047": "estrela", "0049": "frederico_westphalen", "0051": "garibaldi", "0052": "guaiba", "0055": "jaguarao", "0057": "lagoa_vermelha", "0059": "osorio", "0061": "quarai", "0063": "santa_vitoria_palmar", "0064": "santiago", "0068": "sao_sebastiao_cai", "0071": "taquari", "0072": "torres", "0073": "tramandai", "0075": "tres_passos", "0078": "veranopolis", "0080": "arroio_meio", "0086": "cachoeirinha", "0087": "campo_bom", "0093": "coronel_bicaco", "0094": "crissiumal", "0097": "flores_cunha", "0098": "gaurama", "0102": "guarani_missoes", "0104": "horizontina", "0109": "marau", "0113": "nonoai", "0124": "santo_cristo", "0130": "sao_sepe", "0138": "tenente_portela", "0139": "triunfo", "0140": "barra_ribeiro", "0146": "feliz", "0152": "sao_valentim", "0153": "tucunduva", "0156": "charqueadas", "0157": "parobe", "0158": "rodeio_bonito", "0078": "veranopolis", "0038": "vacaria", "0026": "santa_cruz_sul", "0041": "canela", "0089": "candelaria", "0070": "taquara"}

dicionario_themis = {x.replace("0","",1): dicionario_cnj[x] for x in dicionario_cnj.keys()}

dicionario_cnj = defaultdict(lambda: 'todas', dicionario_cnj)
dicionario_themis = defaultdict(lambda: 'todas', dicionario_themis)




class AcessarSite():
    def __init__(self):
        self.resultado = {"Consultado": [], "Extraido": [], "Comarca": [], "O_Julgador": [], "Procedimento": [],
             "Ativa": [], "E_Ativa": [], "Passiva": [], "E_Passiva": []}
        self.time = datetime.now().strftime('%Y%m%d%H%M%S')
    def novo_acesso(self):
        self.sessao = requests.Session()
        self.url = "https://www.tjrs.jus.br/site_php/consulta/verifica_codigo_novo.php"

    



    def pegar_captcha(self):
        urlimg = "https://www.tjrs.jus.br/site_php/consulta/human_check/humancheck_showcode.php"
        response = self.sessao.get(urlimg)
        if response.status_code == 200:
            with open("1.png", 'wb') as f:
                f.write(response.content)
        else:
            return None
        image = Image.open('1.png')
        return image

    def get_comarca(self, codigoConsulta, cnj):
        if(cnj == 'S'):
            return dicionario_cnj[codigoConsulta[0][-4:]]
        else:
            #return dicionario_themis[ codconsulta[0].split('/')[0] ]
            return dicionario_themis[codigoConsulta[0][0:3]]

    def check_if_cnj(self, codigoConsulta):

        if('/' in codigoConsulta[0]):
            return 'N', 0
        else:
            if('.' in codigoConsulta[0]):
                return 'S', 1
            else:
                return 'N', 2

        

    def make_request(self, codigoConsulta, codigo, debug = True):

        cnj, qual = self.check_if_cnj(codigoConsulta)
        comarca = self.get_comarca(codigoConsulta, cnj)
        if(qual == 0):
            result = self.sessao.get(self.url, params={"tipo": 1, "id_comarca": comarca,
                                            "N1_var2":1, "num_processo":re.sub("[^0-9]", "", codigoConsulta[0][3:]),
                                            "numCNJ":cnj, "code":codigo})
        else:
            result = self.sessao.get(self.url, params={"tipo": 1, "id_comarca": comarca,
                                            "N1_var2":1, "num_processo":re.sub("[^0-9]", "", codigoConsulta[0]),
                                            "numCNJ":cnj, "code":codigo})

        if(debug):
            print('\n', result.url)
        return result


    def get_data(self, result, codigoConsulta):
        
        root = html.fromstring(unicodedata.normalize("NFKD", result.text))
        tree = etree.ElementTree(root)


        procedimento = tree.xpath(
            '//*[@id="conteudo"]/table[2]/tr[1]/td[2]/text()')
        extraido = tree.xpath('/html/body/div/table[1]/tr/td[3]/text()')
        comarca = tree.xpath('/html/body/div/table[3]/tr[1]/td[3]/text()')
        o_julgador = tree.xpath('/html/body/div/table[3]/tr[2]/td[3]/text()')
        ativa = tree.xpath('/html/body/div/table[5]/tr[2]/td[2]/text()')
        e_ativa = tree.xpath('/html/body/div/table[5]/tr[2]/td[3]/text()')

        def checar_dois_pontos_numero(asd):
            chars = set('0123456789:')
            if(len(asd) > 0):
                if any((c in chars) for c in asd[0]):
                    return True
                else:
                    return False
            else:
                return True

        passiva = tree.xpath('//*[@id="conteudo"]/table[5]/tr[3]/td[2]/text()')
        e_passiva = tree.xpath('/html/body/div/table[5]/tr[3]/td[3]/text()')
        for i in range(3,10):
            passiva = tree.xpath('//*[@id="conteudo"]/table[5]/tr['+str(i)+']/td[2]/text()')
            e_passiva = tree.xpath('/html/body/div/table[5]/tr['+str(i)+']/td[3]/text()')
            if(not checar_dois_pontos_numero(e_passiva)):
                break
        self.resultado["Procedimento"].append(procedimento[0] if len(procedimento) > 0 else None)
        self.resultado["Consultado"].append(codigoConsulta[0])
        self.resultado["Extraido"].append(extraido[0] if len(extraido) > 0 else codigoConsulta[0])
        self.resultado["Comarca"].append(comarca[0] if len(comarca) > 0 else None)
        self.resultado["O_Julgador"].append(o_julgador[0] if len(o_julgador) > 0 else None)
        self.resultado["Ativa"].append(ativa[0] if len(ativa) > 0 else None)
        self.resultado["E_Ativa"].append(e_ativa[0] if len(e_ativa) > 0 else None)
        self.resultado["Passiva"].append(passiva[0] if len(passiva) > 0 else None)
        self.resultado["E_Passiva"].append(e_passiva[0] if len(e_passiva) > 0 else None)
        


    def save_data(self):
        df = pandas.DataFrame.from_dict(self.resultado)
        #df.to_csv("ListaFinal.csv",sep=";",encoding='utf-8-sig',index=False)
        df.to_excel(f"{self.time}.xlsx",header=True, index=False)
