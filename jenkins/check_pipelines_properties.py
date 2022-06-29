import os
import json
from dotenv import dotenv_values
import xml.etree.ElementTree as ET

config = {**dotenv_values()}
folder = config.get('FOLDER')
stage = config.get('STAGE')
tenant = config.get('TENANT')
database = config.get('DATABASE')


def getTenantStageJson():
    return f'{database}/{tenant}/{stage}_{tenant}_jenkins.json'


def readDb(database, ext='json'):
    data = []

    if os.path.exists(database):
        with open(database, 'r', encoding='utf8') as f:
            if ext == 'xml':
                data = ET.fromstring(f.read())
            elif ext == 'json':
                data = json.loads(f.read())
            else:
                data = f.read()

    return data


def write(objects, db, isJson=0, retry=2):
    try:
        wObjetcs = objects
        if isJson:
            wObjetcs = json.dumps(objects, indent=4)

        if os.path.exists(db):
            with open(db, 'w', encoding='utf8') as f:
                f.write(wObjetcs)
        else:
            os.system(f'touch {db}')
            if retry > 0:
                write(objects, db, retry - 1)
            else:
                print('Arquivo não existe!')
    except Exception as e:
        print(f'Não foi possível escrever!\nArquivo: {db}')


def main():


main()
