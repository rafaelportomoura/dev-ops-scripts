import os
import json
db = 'database/repositories.json'

NULL = 0


def writeRepositories(objects, db, retry=0):
    try:
        json_object = json.dumps(objects, indent=4)

        if os.path.exists(db):
            with open(db, 'w', encoding='utf8') as f:
                f.write(json_object)
        else:
            os.system(f'touch {db}')
            if retry < 2:
                writeRepositories(objects, db, retry + 1)
            else:
                print('Arquivo não existe!')
    except Exception as e:
        print('Não foi possível escrever!')


def pwd():
    pwd = os.path.realpath(os.getcwd())
    return pwd


def getFilePath(tenant, name):
    return f'..\CodeCommit\\{tenant}\\{name}'


def readDb(database, isJson=1):
    data = []

    if os.path.exists(database):
        with open(database, 'r', encoding='utf8') as f:
            if isJson:
                data = json.loads(f.read())
            else:
                return f.read()

    return data


def ls(path='.'):
    array = []
    ls = os.listdir(path)
    for entry in ls:
        if (entry != 'ls.exe.stackdump'):
            array.append(entry)
    return array


def chdir(path):
    os.chdir(path)


def getResources(path, template):
    file = readDb(f'{path}\{template}', 0)
    lines = file.rsplit('\n')
    count = 0
    resources = []
    for line in lines:
        if 'Type: AWS::' in line:
            resources.append(
                {"name": lines[count - 1].replace(':', '').replace('  ', ''), "type": line.replace('    Type: ', '')})
        count += 1
    return resources


def checkout(_branch_):
    os.system(f'git checkout {_branch_}')
    os.system(f'git pull origin {_branch_}')


repositories = readDb(db)

resources = {}

for repository in repositories:
    name = repository.get('repositoryName')
    tenant = repository.get('tenant')
    if tenant == 'core':
        _ = pwd()
        path = getFilePath(tenant, name)
        print(name)
        resources[name] = {
            "template": NULL,
            "resources": []
        }
        try:
            chdir(f'{path}\\templates')
            checkout('master')
            resources[name]["template"] = ls()[0]
            resources[name]["resources"] = getResources(
                pwd(), resources[name]["template"])
        except Exception as e:
            print('Não possui template')
        print('\n')
        chdir(_)

writeRepositories(resources, 'database/resources.json')
