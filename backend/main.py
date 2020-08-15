import logging
import os
import traceback

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
logging.getLogger("tensorflow").disabled = True

import sys
import time
import unicodedata

import numpy as np
import pandas
import uvicorn
from scrapper_tjrs.app import app
from scrapper_tjrs.captcha import CaptchaSolver
from scrapper_tjrs.tjrs import TJRS
from tqdm import tqdm

if __name__ == "__main__":
    uvicorn.run("scrapper_tjrs.app:app", port=8000, reload=True)
