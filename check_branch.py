import json
import os
from dotenv import dotenv_values
config = {**dotenv_values()}
profile = config.get('PROFILE')
region = config.get('REGION')

# FUNCTIONS


def readDb(database='database/repositories.json'):
    data = []

    if os.path.exists(database):
        with open(database, 'r', encoding='utf8') as f:
            data = json.loads(f.read())

    return data


def check_repository_branch(_repository, _branch):
    have_branch = bool(0)
    try:
        json.loads(os.popen(
            f'aws codecommit get-branch --profile {profile} --repository-name {_repository} --branch-name {_branch}').read())
        have_branch = bool(1)
        print(f'\t[{_branch}]: ✅')
        _message = f'\t[{_branch}]: ✅'
    except Exception as e:
        print(f'\t[{_branch}]: ❌')
        _message = f'\t[{_branch}]: ❌'
    return [have_branch, _message]


def check_branchs(_name, _branchs):
    branch_output = {}
    repository_message = f'{name}\n'
    for branch in _branchs:
        branch_output[branch] = {}
        [have_branch, message] = check_repository_branch(_name, branch)
        branch_output[branch] = have_branch
        repository_message += f'{message}\n'
    return [branch_output, repository_message]


def writeRepositories(objects, ext='json', db='database/repositories_branch_outputs.json'):
    if ext == 'json':
        objects = json.dumps(objects, indent=4)

    if os.path.exists(db):
        with open(db, 'w', encoding='utf8') as f:
            f.write(objects)
    else:
        raise Exception('Arquivo não existe!')
# MAIN


branchs = ['develop', 'qa', 'homolog', 'master',
           'feature/ic-3911', 'feature/ic-3911-dev', 'feature/ic-3911-qa']
repositories = readDb()
tenant = 'btg-layer'
output = {}
text_output = ''
for repository in repositories:
    name = repository['repositoryName']

    print(f'{name}')
    if repository['tenant'] == tenant:
        [output[name], text] = check_branchs(name, branchs)
        text_output += f'{text}\n'

print(output)
writeRepositories(output)
writeRepositories(text_output, 'txt',
                  'database/repositories_branch_outputs.txt')
