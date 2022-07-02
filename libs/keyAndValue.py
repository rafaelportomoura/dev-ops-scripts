class ArgvKeyValueParser:
    def __init__(self, args):
        self.args = args
        self.parseToDict()

    def __str__(self):
        return f"{self.dict_args}"

    def parseToDict(self):
        self.dict_args = {}
        self.dict_args['strings'] = []
        for arg in self.args:
            if '=' in arg:
                [key, value] = arg.split('=')
                self.dict_args[key] = value
            else:
                self.dict_args['strings'].append(arg)

    def getArgs(self):
        return self.dict_args
