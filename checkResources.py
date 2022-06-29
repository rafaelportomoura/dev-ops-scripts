import os
import json
db = 'database/resources.json'

NULL = 0


def writeRepositories(objects, db, retry=2, isJson = 1):
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
        writeRepositories(objects, db, retry - 1)
      else:
        print('Arquivo não existe!')
  except Exception as e:
    print('Não foi possível escrever!')


def readDb(database, isJson=1):
    data = []

    if os.path.exists(database):
        with open(database, 'r', encoding='utf8') as f:
          if isJson:
            data = json.loads(f.read())
          else:
            return f.read()
            
    return data

def createTaskList(name,resources):
  taskList = f'## {name}\n'
  for resource in resources:
    taskList += f'[{resource["type"]}] {resource["name"]}\n\n'
  return taskList


repositories = readDb(db)
text = ''
for repository in repositories:
  text += createTaskList(repository, repositories[repository]["resources"])
  text += '\n'


print(text)

writeRepositories(text,'database/checkResources.txt',0)