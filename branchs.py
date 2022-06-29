import os
import json
import time
from dotenv import dotenv_values
config ={**dotenv_values()}
profile = config.get('PROFILE')
region = config.get('REGION')
database = 'database/repositories.json'
BRANCH = 'homolog'


def ls(path='.'):
  array = []
  ls =  os.listdir(path)
  for entry in ls:
    if (entry != 'ls.exe.stackdump'):
      array.append(entry)
  return array
def getFilePath(_file_path_):
  return f'..\CodeCommit\{_file_path_}'
  
def remove_node_modules():
  os.system('rm -rf node_modules')

def chdir(path):
  os.chdir(path)

def yarn():
  os.system(f'yarn')

def merge_squash(_branch_):
  os.system(f'git merge --squash {_branch_}')

def create_branch(_branch_):
  os.system(f'git checkout -b {_branch_}')

def commit(message):
  os.system(f'git commit -m "{message}"')

def commit_husky():
  os.system(f'git commit')

def git_push(remote,branch):
  os.system(f'git push --set-upstream {remote} {branch} --no-verify')

def git_pull(remote,_branch_):
  os.system(f'git pull {remote} {_branch_}')

def checkout( _branch_):
  os.system(f'git checkout {_branch_}')


def clone(repository, path):
  os.system(f'git clone codecommit://{profile}@{repository} {path}\{repository}')

def readDb(db, isJson=1):
    data = []

    if os.path.exists(db):
        with open(db, 'r', encoding='utf8') as f:
          if isJson:
            data = json.loads(f.read())
          else:
            return f.read()

    return data

def writeDb(writer, db, isJson=1):
    json_object = writer
    if isJson:
      json_object = json.dumps(writer, indent=4)

    if os.path.exists(db):
        with open(db, 'w', encoding='utf8') as f:
            f.write(json_object)
    else:
        raise Exception('Arquivo não existe!')

def getResources():
  os.system('python getResources.py')
  resources = readDb('database/resources.json')
  return resources

repositories = readDb(database)

def imprimi(message):
  print(f'- [{message}] -')

for repository in repositories:
  name = repository.get('repositoryName')
  tenant = repository.get('tenant')
  if tenant == 'btg-layer':
    print(f'\n\n\t\t[{name}]\n')
    path = getFilePath(f'{tenant}\{name}')
    chdir(path)
    checkout('homolog')
    git_pull('origin','homolog')
    chdir('..\\..\\..\\aws scripts')
