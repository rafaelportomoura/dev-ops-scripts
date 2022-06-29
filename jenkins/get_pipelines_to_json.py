import os
import json
import time
from dotenv import dotenv_values
import xml.etree.ElementTree as ET

config = {**dotenv_values()}
folder = config.get('FOLDER')
stage = config.get('STAGE')
tenant = config.get('TENANT')
database = config.get('DATABASE')


def getTenantStageFolder():
    return f'{folder}/{tenant}/jobs/{stage}/jobs'


def ls(path='.'):
    array = []
    ls = os.listdir(path)
    for entry in ls:
        if (entry != 'ls.exe.stackdump'):
            array.append(entry)
    return array


def getJobs(path):
    jobs = ls(path)
    return jobs


def readDb(database, ext='xml'):
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


def checkIfSavetag(tag):
    return tag == 'name' or tag == 'defaultValue'


def getResources(job_path):
    job = readDb(job_path, 'xml')
    resources = {}
    parameter_name = ''
    for child in job.iter():
        if child.tag == 'properties':
            resources['properties'] = {}
            for tag in child.iter():
                if checkIfSavetag(tag.tag):
                    if (tag.tag == 'name'):
                        parameter_name = tag.text
                        resources['properties'][parameter_name] = ''
                    if (tag.tag == 'defaultValue'):
                        resources['properties'][parameter_name] = tag.text

    return resources


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


def remove_builds(path):
    os.system(f'rm -rf {path}/scm-polling.log')
    os.system(f'rm -rf {path}/builds')
    os.system(f'rm -rf {path}/nextBuildNumber')


def main():
    root_folder = getTenantStageFolder()
    jobs = getJobs(root_folder)
    jobs_resources = {}
    for job in jobs:
        jobs_resources[job] = getResources(f'{root_folder}/{job}/config.xml')
        remove_builds(f'{root_folder}/{job}')
    write(jobs_resources,
          f'{database}/{tenant}/{stage}_{tenant}_jenkins.json', 1)


main()
