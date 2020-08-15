import io
import logging
import os
import re
import unicodedata
import urllib
from datetime import datetime
from urllib.request import urlopen

import cv2
import numpy as np
import pandas
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from lxml import etree, html
from PIL import Image
from requests import session

from .comarcas import dict_cnj, dict_themis
from .model import Process, SessionLocal


class TJRS:
    def __init__(self):
        self.headers = UserAgent()
        self.proxy = dict(https="socks5://gYqYWk:pMbDhL@185.59.234.197:8000",)
        self.time = datetime.now().strftime("%Y%m%d%H%M%S")
        self.url = "https://www.tjrs.jus.br/site_php/consulta/verifica_codigo_novo.php"
        self.session = None

    def new_access(self):
        self.session = requests.Session()

    def get_captcha(self):
        urlimg = "https://www.tjrs.jus.br/site_php/consulta/human_check/humancheck_showcode.php"
        response = self.session.get(
            urlimg,
            headers={"User-Agent": str(self.headers.random)},
        )
        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            return image
        return None

    def get_comarca(self, process_num, cnj):
        if cnj == "S":
            return dict_cnj[process_num[-4:]]
        else:
            return dict_themis[process_num[0:3]]

    def get_process_num_type(self, process_num):
        """Checks the type of the process number
        If the process number has . and / or nothing it's themis
        If the process number has just a . it's a cnj
        Note:
        0 for a themis with /
        1 for cnj
        2 for themis without /
        Args:
            process_num (str): process number

        Returns:
            (str, int): num_cnj and process number type
        """
        if "/" in process_num:
            return "N", 0
        else:
            if "." in process_num:
                return "S", 1
        return "N", 2

    def make_request(self, process_num, captcha):
        num_cnj, process_num_type = self.get_process_num_type(process_num)

        comarca = self.get_comarca(process_num, num_cnj)

        params = {
                    "tipo": 1,
                    "id_comarca": comarca,
                    "N1_var2": 1,
                    "num_processo": re.sub("[^0-9]", "", process_num[3:] if not process_num_type else process_num),
                    "numCNJ": num_cnj,
                    "code": captcha,
                }

        result = self.session.get(
            self.url,
            params=params,
            headers={"User-Agent": str(self.headers.random)},
        )

        logging.debug(result.url)

        return result

    def get_data(self, result, process_num):
        root = html.fromstring(unicodedata.normalize("NFKD", result.text))
        tree = etree.ElementTree(root)

        procedimento = tree.xpath('//*[@id="conteudo"]/table[2]/tr[1]/td[2]/text()')
        extraido = tree.xpath("/html/body/div/table[1]/tr/td[3]/text()")
        comarca = tree.xpath("/html/body/div/table[3]/tr[1]/td[3]/text()")
        o_julgador = tree.xpath("/html/body/div/table[3]/tr[2]/td[3]/text()")
        ativa = tree.xpath("/html/body/div/table[5]/tr[2]/td[2]/text()")
        e_ativa = tree.xpath("/html/body/div/table[5]/tr[2]/td[3]/text()")

        def check_colon_number(value):
            chars = set("0123456789:")
            if len(value) > 0:
                if any((c in chars) for c in value):
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
            if not check_colon_number(e_passiva[0]):
                break

        p = Process()

        p.procedimento =  procedimento[0].strip() if len(procedimento) > 0 else None
        p.consultado = process_num.strip()
        p.extraido = extraido[0].strip() if len(extraido) > 0 else process_num
        p.comarca = comarca[0].strip() if len(comarca) > 0 else None
        p.o_julgador = o_julgador[0].strip() if len(o_julgador) > 0 else None
        p.ativa = ativa[0].strip() if len(ativa) > 0 else None
        p.e_ativa = e_ativa[0].strip() if len(e_ativa) > 0 else None
        p.passiva = passiva[0].strip() if len(passiva) > 0 else None
        p.e_passiva = e_passiva[0].strip() if len(e_passiva) > 0 else None
        p.created = self.time

        return p
