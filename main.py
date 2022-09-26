import time

import uvicorn
from fastapi import FastAPI, UploadFile
from fastapi.responses import FileResponse
import configparser
import shutil
import os

app = FastAPI()
Token = 123

config = configparser.ConfigParser()
config.read('conf.ini')
PATH = config['APP']['path']


@app.post("/upload")
def upload(file: UploadFile):
    time.sleep(4)
    if ".zip" in file.filename:
        upload_url = os.path.dirname(os.path.abspath(__file__))
        PATH = config['APP']['path']
        os.remove(os.path.join(upload_url, PATH))
        config['APP']['path'] = file.filename
        PATH = file.filename
        file_object = file.file
        # create empty file to copy the file_object to
        upload_folder = open(os.path.join(upload_url, file.filename), 'wb+')
        shutil.copyfileobj(file_object, upload_folder)
        upload_folder.close()
        config['APP']['path'] = file.filename
        with open('conf.ini', 'w') as configfile:  # save
            config.write(configfile)
        return f"File {config['APP']['path']} is uploaded"
    else:
        return "Wrong format"


@app.get("/info")
async def info():
    from os import walk

    filenames = next(walk(os.path.dirname(os.path.abspath(__file__))), (None, None, []))[2]  # [] if no file
    return f"filenames {filenames}, config: {config['APP']['path']}, PATH {PATH}"


@app.get("/file", response_class=FileResponse)
async def main():
    print('debug')
    time.sleep(2)
    print(config['APP']['path'])
    print(PATH)
    return config['APP']['path']


if __name__ == '__main__':
    uvicorn.run(app=app)
