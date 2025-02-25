from .exceptions import VaultExceptions
from utils.backup import Backup

# TODO сделать проверку на старые записи

class Vault:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.backup = Backup()
        self.__vault = {}
        data = self.backup.load()
        if data:
            self.__vault = data


    def __del__(self):
        self.backup.save(self.__vault)

    def append(self, other: dict[str, str, str]):
        date, subj, text = other['date'], other['subj'], other['text']
        self.__vault.setdefault(date, []).append((subj, text))

    def get(self, date: str) -> list:
        data = self.__vault.get(date, [])
        if not data:
            error_text = "Value {0} not found. Function get"
            raise VaultExceptions(error_text.format(date))
        return data

    def pop(self, date: str) -> list:
        data = self.__vault.pop(date, [])
        if not data:
            error_text = "Value {1} not found. Function pop"
            raise VaultExceptions(error_text.format(date))
        return data

    def get_format(self, date: str, forced: int = 0) -> str:
        data = self.get(date) if forced else self.pop(date)
        if not data:
            error_text = "Value {1} not found. Function get_format"
            raise VaultExceptions(error_text.format(date))
        base = "News at <b>{0}({1})</b>:\n".format(date, len(data))
        subjects_dict = {}

        for news in sorted(data):
            subjects_dict.setdefault(news[0], []).append(news[1])

        for key in subjects_dict.keys():
            information = '  · ' + '\n  · '.join(subjects_dict[key])
            base += key + '\n' + information + '\n'
        return base

    def get_coming_days(self, dates_arr: set) -> set:
        dates = set(self.__vault.keys())
        return dates & dates_arr

    def date_exist(self, date: str) -> bool:
        return date in self.__vault.keys()
