import os
import json
import sys
from dotenv import dotenv_values
config = {**dotenv_values()}
profile = config.get('PROFILE')
region = config.get('REGION')
database = 'database/repositories.json'
ACCOUNT = config.get('ACCOUNT')

path_delimiter = os.path.sep


def ls(path='.'):
    array = []
    ls = os.listdir(path)
    for entry in ls:
        if (entry != 'ls.exe.stackdump'):
            array.append(entry)
    return array


def getFilePath(_file_path_, _=path_delimiter):
    path = f'..{_}Accounts{_}{ACCOUNT}{_}CodeCommit'
    file_path = f'{path}{_}{_file_path_}'
    tenants = ls(path)
    has = False
    for t in tenants:
        if t == _file_path_:
            has = True

    if not has:
        os.mkdir(file_path)

    return file_path


def clone(repository, path, _=path_delimiter):
    os.system(
        f'git clone codecommit://{profile}@{repository} {path}{_}{repository}')


def readDb():
    data = []

    if os.path.exists(database):
        with open(database, 'r', encoding='utf8') as f:
            data = json.loads(f.read())

    return data


repositories = readDb()

for repository in repositories:
    tenant = repository.get('tenant')
    name = repository.get('repositoryName')
    path = getFilePath(tenant, path_delimiter)
    folders = ls(path)
    x = 0
    for folder in folders:
        if name in folder:
            x = 1
    if not x:
        print(f'[CLONE]: {tenant}/{name}')
        clone(name, path, path_delimiter)
    else:
        print(f'[DISCARDED]: {tenant}/{name}')
