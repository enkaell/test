from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from dataclasses import dataclass

import datetime
import shutil

app = FastAPI()
Token = 123


@dataclass
class Path:
    path: str


info = Path('ostatki.zip')


@app.get("/", response_class=FileResponse)
async def main():
    return Path.path


@app.post("/upload")
def upload(file: UploadFile):
    if ".zip" in file.filename:
        with open(file.filename, 'wb') as f:
            shutil.copyfileobj(file.file, f)
        Path.path = str(file.filename)
        info.time = datetime.datetime.now()
        return f"File {Path.path} is uploaded"
    else:
        return "Wrong format"


@app.get("/info")
async def main():
    return f"Updated at {info.time}"
