import json
import os
from dotenv import dotenv_values
config = {**dotenv_values()}
profile = config.get('PROFILE')
region = config.get('REGION')


def readDb(database):
    data = []

    if os.path.exists(database):
        with open(database, 'r', encoding='utf8') as f:
            data = json.loads(f.read())

    return data


def get_conflicts(_repository, _origin_branch, _target_branch, _merge_type='THREE_WAY_MERGE'):
    conflicts = json.loads(os.popen(
        f'aws codecommit get-merge-conflicts --profile {profile} --region {region} --repository-name {_repository} --source-commit-specifier {_origin_branch} --destination-commit-specifier {_target_branch} --merge-option {_merge_type}').read())

    return conflicts


def mergeable(_repository, _origin_branch, _target_branch):
    conflicts = get_conflicts(_repository, _origin_branch, _target_branch)
    return conflicts['mergeable']


def verify_repositories_branchs(_origin_branch, _target_branch, _repository):
    has_origin_branch = _origin_branch in _repository and _repository[_origin_branch]
    has_target_branch = _target_branch in _repository and _repository[_target_branch]
    message = ''
    if not has_origin_branch:
        message += f'\t\t❌ [BRANCH] Repositorio não possui {_origin_branch}\n'
    if not has_target_branch:
        message += f'\t\t❌ [BRANCH] Repositorio não possui {_target_branch}\n'

    return [has_origin_branch and has_target_branch, message]


def create_report(_name, _origin_branch, _target_branch, _repository):
    [have_branchs, message] = verify_repositories_branchs(
        _origin_branch, _target_branch, _repository)
    if not have_branchs:
        return [message, 0]

    if mergeable(_name, _origin_branch, _target_branch):
        return ['\t\t✅ MERGEAVEL\n', 1]

    return ['\t\t❌ [NÃO MERGEAVEL] Possui conflito\n', 0]


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


repositories = readDb('database/repositories_branch_outputs.json')

branchs = [
    {
        'origin': 'feature/ic-3911-dev',
        'target': "develop"
    },
    {
        'origin': 'feature/ic-3911-qa',
        'target': "qa"
    },
    {
        'origin': 'feature/ic-3911',
        'target': "homolog"
    }
]

output_message = ''
output = {}

for name in repositories:
    count = 0
    output[name] = {}
    output[name]['merges'] = []
    output_message += f'{name}\n'
    print(name)
    for branch in branchs:
        print(f'\t{branch["origin"]} -> {branch["target"]}')
        output_message += f'\t{branch["origin"]} -> {branch["target"]}\n'
        [message, is_mergeable] = create_report(name,
                                                branch['origin'], branch['target'], repositories[name])

        output[name]['merges'].append({
            'origin': branch['origin'],
            'target': branch['target'],
            'mergeable': is_mergeable
        })
        print(message)
        output_message += message
        output_message += '\n'
        count += 1
    output_message += '---------------------------------------------------------------------------------------\n\n'


write(output_message,
      'database/conflicts_report.txt')

write(output,
      'database/conflicts_report.json', 1)
