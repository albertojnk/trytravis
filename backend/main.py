import logging
import os
import traceback

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logging.getLogger("tensorflow").disabled = True

import numpy as np
import pandas
import time
import unicodedata
import sys

from scrapper_tjrs.tjrs import TJRS
from scrapper_tjrs.captcha import CaptchaSolver
from tqdm import tqdm


solver = CaptchaSolver()
tjrs = TJRS()


perinni = pandas.read_excel(
    "data/1.xlsx", usecols="A", sheet_name="1", converters={"processos": lambda x: str(x)}
)
process_list = perinni.values.tolist()

checkpoint = 0
if os.path.exists("checkpoint.txt"):
    with open("checkpoint.txt", "r") as check:
        checkpoint = int(check.read())
        process_list = process_list[checkpoint:]

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

        tjrs.get_data(result, process_num[0])

    except Exception as e:
        traceback.print_exc()
        with open("checkpoint.txt", "w") as check:
            check.write(str(i+checkpoint))
        sys.exit("batatinha")
    except KeyboardInterrupt:
        with open("checkpoint.txt", "w") as check:
            check.write(str(i+checkpoint))
        sys.exit("perinni")

print("Total: {}".format(total), "captchas")
print("Misses: {}".format(miss), "captchas")
print("Hits: {}%".format((1 - miss / total) * 100))
if os.path.exists("checkpoint.txt"):
   os.remove("checkpoint.txt")
