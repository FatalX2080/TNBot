class Vault:
    class Dispatcher:
        _instance = None

        def __new__(cls, *args, **kwargs):
            if not cls._instance:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self):
        self.__vault = {}

    def append(self, other):
        date, subj, text = other.info()
        self.__vault.setdefault(date, []).append((subj, text))
        print(self.__vault)

    def get(self, date):
        return self.__vault.pop(date, None)

    def pop(self, date):
        return self.__vault.pop(date, None)

    def get_format(self, date):
        data = self.pop(date)
        if not data:
            return None
        data.sort()
        base = "News at {0}({1})\n".format(date, len(data))
        subjects_dict = {}
        for news in sorted(today_news):
            subjects_dict.setdefault(news[0], []).append(news[1])

        for key in subjects_dict.keys():
            information = '· ' + '\n· '.join(subjects_dict[key])
            base += key + '\n' + information + '\n'
        return base
