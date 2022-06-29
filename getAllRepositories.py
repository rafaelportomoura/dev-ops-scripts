import os
import json
from dotenv import dotenv_values
config ={**dotenv_values()}
profile = config.get('PROFILE')
region = config.get('REGION')

database = 'database/repositories.json'


def listRepositories():
  try:
    return json.loads(os.popen(f'aws codecommit list-repositories --profile {profile} --region={region}').read())
  except Exception as e:
    print(e)

def writeRepositories(objects, db):
    json_object = json.dumps(objects, indent=4)

    if os.path.exists(db):
        with open(db, 'w', encoding='utf8') as f:
            f.write(json_object)
    else:
        raise Exception('Arquivo não existe!')


def get_repository(_repository):
    return json.loads(os.popen(f'aws codecommit get-repository  --profile {profile} --repository-name {_repository}').read())


def list_tags_for_resource(_arn):
    return json.loads(os.popen(f'aws codecommit list-tags-for-resource  --profile {profile} --resource-arn {_arn}').read())


def get_repository_arn(_repository):
    repository_data = get_repository(_repository)
    repositoryMetadata = repository_data['repositoryMetadata']
    return repositoryMetadata['Arn']


def get_repository_tags(_repository):
    arn = get_repository_arn(_repository)
    resource = list_tags_for_resource(arn)
    return resource['tags']

repositories = listRepositories().get('repositories')

core = []
btg_layer = []
outros = []

for repository in repositories:
  name = repository['repositoryName']
  tags = get_repository_tags(name)
  if 'boilerplate' in name:
    repository['tenant'] = 'boilerplate'
  elif 'tenant' in tags:
    repository['tenant'] = tags['tenant']
  else:
    repository['tenant'] = 0
  
  print(f'[{repository["tenant"]}]: {name}')



writeRepositories(repositories, database)
# writeRepositories(core, 'core.json')
# writeRepositories(btg_layer, 'btg-layer.json')
# writeRepositories(outros, 'outros.json')



print(repositories)