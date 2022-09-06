import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import zipfile
from fastapi import FastAPI, BackgroundTasks, UploadFile
from fastapi.responses import FileResponse
from urllib.request import urlopen
from lxml import etree

import datetime
import shutil

path = 'ostatki.zip'
app = FastAPI()
Token = 123


@app.get("/", response_class=FileResponse)
async def main():
    return path


@app.post("/upload")
def upload(file: UploadFile):
    if ".xml" in file.filename:
        with open(file.filename, 'wb') as f:
            shutil.copyfileobj(file.file, f)
        zf = zipfile.ZipFile("ostatki.zip", "w", compresslevel=8, compression=zipfile.ZIP_DEFLATED)
        zf.write(file.filename, compresslevel=8)
        return "File is uploaded"
    else:
        return "Wrong format"
