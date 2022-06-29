import os
import json
from dotenv import dotenv_values
config = {**dotenv_values()}
profile = config.get('PROFILE')
region = config.get('REGION')

aprovers = {
    'develop': '830158993455579147',
    'qa': '882673985102417930',
    'homolog': '882674279622258708',
    'master': '882674518877949973'
}


def create_pull_request(repository, source, destination, description):
    result = json.loads(os.popen(
        f'aws codecommit --profile {profile} create-pull-request --region {region} --title "{description}" --targets repositoryName={repository},sourceReference={source},destinationReference={destination}').read())
    return result


def create_message(branch, description, url, group_id):
    message = f'[{branch}] {description}\n'
    message += url
    message += f'\n<@&{group_id}>\n\n'
    print(message)
    return message


def create_url(repository, pr_id):
    pr_url = f'https://{region}.console.aws.amazon.com/codesuite/codecommit/repositories/{repository}/pull-requests/{pr_id}/details?region={region}'
    return pr_url


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


def writeMessages(messages):
    db = 'database/prs.txt'
    write(messages, db)


def readDb(db):
    data = []

    if os.path.exists(db):
        with open(db, 'r', encoding='utf8') as f:
            data = json.loads(f.read())

    return data


def savePrs(objects):
    db = 'database/prs.json'
    write(objects, db, 1)


def return_message(_target, _origin, _name, _description, _mergeable=0):
    if not _mergeable:
        return ''

    result = create_pull_request(
        _name, _origin, _target, f'[{_name}] {_description}')

    pr_id = result['pullRequest']['pullRequestId']
    url = create_url(name, pr_id)
    aprover = aprovers['develop']
    if _target in aprovers:
        aprover = aprovers[_target]
    message = create_message(_target, name, url, aprover)

    return message


quero = [
    'core-actions'
]

card_code = 'ic-3266-1'

repositories = readDb('database/conflicts_report.json')

description = 'Up core to branch master'

message = ''

ja = readDb('database/prs.json')
print(ja)

for name in repositories:
    repository = repositories[name]
    for pr in repository['merges']:
        target = pr['target']
        origin = pr['origin']
        mergeable = pr['mergeable']
        pr_message = return_message(
            target, origin, name, description, mergeable)
        print(pr_message)
        message += pr_message
        ja.append({
            name: {
                'message': message
            }
        })

savePrs(ja)

writeMessages(message)
