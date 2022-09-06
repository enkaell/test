import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import zipfile
from flask import Flask, send_file
import datetime
import xml.etree.ElementTree as ET

path = 'ostatki.zip'
app = Flask(__name__)
Token = 123


@app.route('/')
def main():
    return send_file(path)


def update_yandex_table():
    print('started')
    json_data = {"password": "RAMTRX1500", "regulation": True, "email": "Rakhmanov-2019@list.ru"}
    response = requests.post('https://www.sima-land.ru/api/v5/signin', json=json_data)
    token = response.json().get('token')
    zip = zipfile.ZipFile('ostatki.zip')
    zip.extractall()
    tree = ET.parse('t.xml')
    root_node = tree.getroot()
    session = requests.Session()
    retry = Retry(connect=2, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    for tag in root_node.findall('shop/offers/offer'):
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
        print(f"{response.json()['sid']} обновлен")
        if int(tag.find('count').text) < 10:
            tag.find('count').text = '0'
        else:
            tag.find('count').text = str(response.json()['balance'])
    tree.write('t.xml', encoding='utf-8')


@app.route('/start')
def start():
    import threading
    threading.Thread(target=update_yandex_table).start()
    return f"Started at {datetime.datetime.now()}"


if __name__ == '__main__':
    app.run(host ='0.0.0.0', port = 5001, debug = True)
