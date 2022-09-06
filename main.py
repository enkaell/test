import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import zipfile
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from urllib.request import urlopen
from lxml import etree

import datetime
import xml.etree.ElementTree as ET


path = 'ostatki.zip'
app = FastAPI()
Token = 123


@app.get("/", response_class=FileResponse)
async def main():
    return path


def update_yandex_table():
    print('started')
    json_data = {"password": "RAMTRX1500", "regulation": True, "email": "Rakhmanov-2019@list.ru"}
    response = requests.post('https://www.sima-land.ru/api/v5/signin', json=json_data)
    token = response.json().get('token')
    print('token initialized')
    session = requests.Session()
    retry = Retry(connect=2, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    print('trying to get xml...')
    var_url = urlopen('https://give-ur-xml.herokuapp.com/')
    print('trying to parse xml...')
    xmldoc = tree = etree.parse(var_url)
    print('starting main loop...')
    for tag in xmldoc.iterfind('shop/offers/offer'):
        try:
            tag.remove(tag[1])
        except Exception:
            pass
        response = session.get(
            f"https://www.sima-land.ru/api/v5/item/{tag.attrib['id']}",
            headers={
                'accept': 'application/json',
                'X-Api-Key': token,
                'Authorization': token,
            },

            params={
                'view': 'brief',
                'by_sid': 'false',
            }
        )
        print(response.json()['sid'])
        if int(tag.find('count').text) < 10:
            tag.find('count').text = '0'
        else:
            tag.find('count').text = str(response.json()['balance'])
    xmldoc.write('t.xml', encoding='utf-8')
    zf = zipfile.ZipFile("ostatki.zip", "w", compresslevel=8, compression=zipfile.ZIP_DEFLATED)
    zf.write('t.xml', compresslevel=8)


@app.get("/start")
async def start(background_tasks: BackgroundTasks):
    background_tasks.add_task(update_yandex_table)
    return f"Started at {datetime.datetime.now()}"

