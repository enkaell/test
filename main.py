import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
from dataclasses import dataclass

import datetime
import shutil
import os

app = FastAPI()
Token = 123


@dataclass
class Path:
    path: str = 'nothing'
    upload_url: str = os.path.dirname(os.path.abspath(__file__))


path = Path()


@app.get("/", response_class=FileResponse)
async def main():
    print('return')
    return path.path


@app.post("/upload")
def upload(file: UploadFile):
    if ".zip" in file.filename:
        file_object = file.file
        # create empty file to copy the file_object to
        upload_folder = open(os.path.join(Path.upload_url, file.filename), 'wb+')
        shutil.copyfileobj(file_object, upload_folder)
        upload_folder.close()
        path.path = file.filename
        return f"File {path.path} is uploaded"
    else:
        return "Wrong format"


@app.get("/info")
async def info():
    return f"Updated at {datetime.datetime.now()}"


if __name__ == '__main__':
    uvicorn.run(app=app)
