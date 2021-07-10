from io import BytesIO
from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile

import fire
import requests

from smart.settings import DATAPATH


def download_and_unzip(url, extract_to="."):
    http_response = urlopen(url)
    zipfile = ZipFile(BytesIO(http_response.read()))
    zipfile.extractall(path=extract_to)


def download(
    url="https://github.com/meghanabhange/smart_content/releases/download/0.01/html.zip",
    save_path=DATAPATH,
):
    download_and_unzip(url, save_path)


fire.Fire(download)
