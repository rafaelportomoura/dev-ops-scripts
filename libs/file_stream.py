import os
import json


class FileStream:

    def __init__(self, databasePath, db, ext='json'):
        self.databasePath = databasePath
        self.db = db
        self.ext = ext
        self.file = self.databasePath + '/' + self.db + '.' + self.ext

    def isJson(self):
        return self.ext == 'json'

    def parseObjectToSave(self, data):
        if self.ext == 'json':
            return json.dumps(data, indent=4)

        return data

    def write(self, data, retry=2):
        try:
            data = self.parseObjectToSave(data)
            if os.path.exists(self.file):
                with open(self.file, 'w', encoding='utf8') as f:
                    f.write(data)
            else:
                os.system(f'touch {self.file}')
                if retry > 0:
                    self.write(data, self.file, retry - 1)
                else:
                    print('Arquivo não existe!')
        except Exception as e:
            print(f'Não foi possível escrever!\nArquivo: {self.file}')
