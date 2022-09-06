import requests
import zipfile
from fastapi import FastAPI, BackgroundTasks, UploadFile
from fastapi.responses import FileResponse
from dataclasses import dataclass

import datetime
import shutil

path = 'ostatki.zip'
app = FastAPI()
Token = 123


@dataclass
class Info:
    time: str


info = Info('default')


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
        info.time = datetime.datetime.now()
        return "File is uploaded"
    else:
        return "Wrong format"


@app.get("/info")
async def main():
    return f"Updated at {info.time}"
