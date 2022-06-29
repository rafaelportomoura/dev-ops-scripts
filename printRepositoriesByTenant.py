import json
import os

database = 'repositories.json'
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
  if tenant == 'core':
    print(name)