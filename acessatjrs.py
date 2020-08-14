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
from fake_useragent import UserAgent

dicionario_cnj = {
    "0001": "porto_alegre",
    "5001": "porto_alegre",
    "2001": "porto_alegre",
    "6001": "porto_alegre",
    "4001": "porto_alegre",
    "9000": "710",
    "0002": "alegrete",
    "0003": "alvorada",
    "0004": "bage",
    "0005": "bento_goncalves",
    "0006": "cachoeira_sul",
    "0007": "camaqua",
    "0008": "canoas",
    "0009": "carazinho",
    "0010": "caxias_sul",
    "0011": "cruz_alta",
    "0012": "dom_pedrito",
    "0013": "erechim",
    "0014": "esteio",
    "0015": "gravatai",
    "0016": "ijui",
    "0017": "lajeado",
    "0018": "montenegro",
    "0019": "novo_hamburgo",
    "0020": "palmeira_missoes",
    "0021": "passo_fundo",
    "0022": "pelotas",
    "0023": "rio_grande",
    "0024": "rio_pardo",
    "0025": "santana_livramento",
    "0026": "santa_cruz_sul",
    "0027": "santa_maria",
    "0028": "santa_rosa",
    "0029": "santo_angelo",
    "0030": "sao_borja",
    "0031": "sao_gabriel",
    "0032": "sao_jeronimo",
    "0033": "sao_leopoldo",
    "0034": "sao_luis_gonzaga",
    "0035": "sapucaia_sul",
    "0036": "soledade",
    "0037": "uruguaiana",
    "0038": "vacaria",
    "0039": "viamao",
    "0040": "cacapava_sul",
    "0041": "canela",
    "0042": "cangucu",
    "0043": "cerro_largo",
    "0044": "encantado",
    "0045": "encruzilhada_sul",
    "0046": "espumoso",
    "0047": "estrela",
    "0048": "farroupilha",
    "0049": "frederico_westphalen",
    "0050": "getulio_vargas",
    "0051": "garibaldi",
    "0052": "guaiba",
    "0053": "guapore",
    "0054": "itaqui",
    "0055": "jaguarao",
    "0056": "julio_castilhos",
    "0057": "lagoa_vermelha",
    "0058": "nova_prata",
    "0059": "osorio",
    "0060": "panambi",
    "0061": "quarai",
    "0062": "rosario_sul",
    "0063": "santa_vitoria_palmar",
    "0064": "santiago",
    "0065": "santo_antonio_patrulha",
    "0066": "sao_francisco_paula",
    "0067": "sao_lourenco_sul",
    "0068": "sao_sebastiao_cai",
    "0069": "sarandi",
    "0070": "taquara",
    "0071": "taquari",
    "0072": "torres",
    "0073": "tramandai",
    "0074": "tres_maio",
    "0075": "tres_passos",
    "0076": "tupacireta",
    "0077": "venancio_aires",
    "0078": "veranopolis",
    "0079": "antonio_prado",
    "0080": "arroio_meio",
    "0081": "arroio_grande",
    "0082": "arvorezinha",
    "0083": "bom_jesus",
    "0084": "butia",
    "0085": "cacequi",
    "0086": "cachoeirinha",
    "0087": "campo_bom",
    "0088": "campo_novo",
    "0089": "candelaria",
    "0090": "casca",
    "0091": "catuipe",
    "0092": "constantina",
    "0093": "coronel_bicaco",
    "0094": "crissiumal",
    "0095": "estancia_velha",
    "0096": "faxinal_soturno",
    "0097": "flores_cunha",
    "0098": "gaurama",
    "0099": "general_camara",
    "0100": "girua",
    "0101": "gramado",
    "0102": "guarani_missoes",
    "0103": "herval",
    "0104": "horizontina",
    "0105": "ibiruba",
    "0106": "irai",
    "0107": "jaguari",
    "0108": "lavras_sul",
    "0109": "marau",
    "0110": "marcelino_ramos",
    "0111": "mostardas",
    "0112": "nao_me_toque",
    "0113": "nonoai",
    "0114": "nova_petropolis",
    "0115": "pedro_osorio",
    "0116": "planalto",
    "0117": "pinheiro_machado",
    "0118": "piratini",
    "0119": "porto_xavier",
    "0120": "sananduva",
    "0121": "santa_barbara_sul",
    "0122": "santo_antonio_missoes",
    "0123": "santo_augusto",
    "0124": "santo_cristo",
    "0125": "sao_francisco_assis",
    "0126": "sao_jose_norte",
    "0127": "sao_jose_ouro",
    "0128": "sao_marcos",
    "0129": "sao_pedro_sul",
    "0130": "sao_sepe",
    "0131": "sao_vicente_sul",
    "0132": "sapiranga",
    "0133": "seberi",
    "0134": "sobradinho",
    "0135": "tapejara",
    "0136": "tapera",
    "0137": "tapes",
    "0138": "tenente_portela",
    "0139": "triunfo",
    "0140": "barra_ribeiro",
    "0141": "capao_canoa",
    "0142": "igrejinha",
    "0143": "arroio_tigre",
    "0144": "carlos_barbosa",
    "0145": "dois_irmaos",
    "0146": "feliz",
    "0147": "restinga_seca",
    "0148": "ronda_alta",
    "0149": "augusto_pestana",
    "0150": "campina_missoes",
    "0151": "palmares_sul",
    "0152": "sao_valentim",
    "0153": "tucunduva",
    "0154": "agudo",
    "0155": "portao",
    "0156": "charqueadas",
    "0157": "parobe",
    "0158": "rodeio_bonito",
    "0159": "teutonia",
    "0160": "vera_cruz",
    "0161": "salto_jacui",
    "0163": "terra_areia",
    "0164": "tres_coroas",
    "0165": "eldorado_sul",
    "0166": "ivoti",
    "7000": "700",
    "9000": "710",
}

dicionario_themis = {
    x.replace("0", "", 1): dicionario_cnj[x] for x in dicionario_cnj.keys()
}

dicionario_cnj = defaultdict(lambda: "todas", dicionario_cnj)
dicionario_themis = defaultdict(lambda: "todas", dicionario_themis)


class AcessarSite:
    def __init__(self):
        self.headers = UserAgent()
        self.proxy = dict(
            https="socks5://gYqYWk:pMbDhL@185.59.234.197:8000",
        )
        self.resultado = {
            "Consultado": [],
            "Extraido": [],
            "Comarca": [],
            "O_Julgador": [],
            "Procedimento": [],
            "Ativa": [],
            "E_Ativa": [],
            "Passiva": [],
            "E_Passiva": [],
        }
        self.time = datetime.now().strftime("%Y%m%d%H%M%S")

    def novo_acesso(self):
        self.sessao = requests.Session()
        self.url = "https://www.tjrs.jus.br/site_php/consulta/verifica_codigo_novo.php"

    def pegar_captcha(self):
        urlimg = "https://www.tjrs.jus.br/site_php/consulta/human_check/humancheck_showcode.php"
        response = self.sessao.get(urlimg, 
        #proxies=self.proxy, 
        headers={'User-Agent':str(self.headers.random)},
        )
        if response.status_code == 200:
            with open("1.png", "wb") as f:
                f.write(response.content)
        else:
            return None
        image = Image.open("1.png")
        return image

    def get_comarca(self, codigoConsulta, cnj):
        if cnj == "S":
            return dicionario_cnj[codigoConsulta[0][-4:]]
        else:
            # return dicionario_themis[ codconsulta[0].split('/')[0] ]
            return dicionario_themis[codigoConsulta[0][0:3]]

    def check_if_cnj(self, codigoConsulta):

        if "/" in codigoConsulta[0]:
            return "N", 0
        else:
            if "." in codigoConsulta[0]:
                return "S", 1
            else:
                return "N", 2

    def make_request(self, codigoConsulta, codigo, debug=True):

        cnj, qual = self.check_if_cnj(codigoConsulta)
        comarca = self.get_comarca(codigoConsulta, cnj)
        if qual == 0:
            result = self.sessao.get(
                self.url,
                params={
                    "tipo": 1,
                    "id_comarca": comarca,
                    "N1_var2": 1,
                    "num_processo": re.sub("[^0-9]", "", codigoConsulta[0][3:]),
                    "numCNJ": cnj,
                    "code": codigo,
                },
                #proxies=self.proxy,
                headers={'User-Agent':str(self.headers.random)},
            )
        else:
            result = self.sessao.get(
                self.url,
                params={
                    "tipo": 1,
                    "id_comarca": comarca,
                    "N1_var2": 1,
                    "num_processo": re.sub("[^0-9]", "", codigoConsulta[0]),
                    "numCNJ": cnj,
                    "code": codigo,
                },
                #proxies=self.proxy,
                headers={'User-Agent':str(self.headers.random)},
            )

        if debug:
            print("\n", result.url)
        return result

    def get_data(self, result, codigoConsulta):

        root = html.fromstring(unicodedata.normalize("NFKD", result.text))
        tree = etree.ElementTree(root)

        procedimento = tree.xpath('//*[@id="conteudo"]/table[2]/tr[1]/td[2]/text()')
        extraido = tree.xpath("/html/body/div/table[1]/tr/td[3]/text()")
        comarca = tree.xpath("/html/body/div/table[3]/tr[1]/td[3]/text()")
        o_julgador = tree.xpath("/html/body/div/table[3]/tr[2]/td[3]/text()")
        ativa = tree.xpath("/html/body/div/table[5]/tr[2]/td[2]/text()")
        e_ativa = tree.xpath("/html/body/div/table[5]/tr[2]/td[3]/text()")

        def checar_dois_pontos_numero(asd):
            chars = set("0123456789:")
            if len(asd) > 0:
                if any((c in chars) for c in asd[0]):
                    return True
                else:
                    return False
            else:
                return True

        passiva = tree.xpath('//*[@id="conteudo"]/table[5]/tr[3]/td[2]/text()')
        e_passiva = tree.xpath("/html/body/div/table[5]/tr[3]/td[3]/text()")
        for i in range(3, 10):
            passiva = tree.xpath(
                '//*[@id="conteudo"]/table[5]/tr[' + str(i) + "]/td[2]/text()"
            )
            e_passiva = tree.xpath(
                "/html/body/div/table[5]/tr[" + str(i) + "]/td[3]/text()"
            )
            if not checar_dois_pontos_numero(e_passiva):
                break
        self.resultado["Procedimento"].append(
            procedimento[0] if len(procedimento) > 0 else None
        )
        self.resultado["Consultado"].append(codigoConsulta[0])
        self.resultado["Extraido"].append(
            extraido[0] if len(extraido) > 0 else codigoConsulta[0]
        )
        self.resultado["Comarca"].append(comarca[0] if len(comarca) > 0 else None)
        self.resultado["O_Julgador"].append(
            o_julgador[0] if len(o_julgador) > 0 else None
        )
        self.resultado["Ativa"].append(ativa[0] if len(ativa) > 0 else None)
        self.resultado["E_Ativa"].append(e_ativa[0] if len(e_ativa) > 0 else None)
        self.resultado["Passiva"].append(passiva[0] if len(passiva) > 0 else None)
        self.resultado["E_Passiva"].append(e_passiva[0] if len(e_passiva) > 0 else None)

    def save_data(self):
        df = pandas.DataFrame.from_dict(self.resultado)
        df.to_csv(f"{self.time}.csv", sep=";", encoding="utf-8-sig", index=False)
        # df.to_excel(f"{self.time}.xlsx", header=True, index=False)
