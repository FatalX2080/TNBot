from bot.handlers.poll import subject_poll
from utils.dt_utils import date_format


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

    def get(self, date):
        return self.__vault.get(date, None)

    def pop(self, date):
        return self.__vault.pop(date, None)

    def get_format(self, date, forced=0):
        data = self.get(date) if forced else self.pop(date)
        if not data: return None
        base = "News at <b>{0}({1})</b>:\n".format(date, len(data))
        subjects_dict = {}

        for news in sorted(data):
            subjects_dict.setdefault(news[0], []).append(news[1])

        for key in subjects_dict.keys():
            information = '  · ' + '\n  · '.join(subjects_dict[key])
            base += key + '\n' + information + '\n'
        return base

    def get_coming_days(self, dates_arr: set):
        dates = set(self.__vault.keys())
        return dates & dates_arr
