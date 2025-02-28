from utils.backup import Backup
from utils.dt_utils import date_comparison
from .exceptions import VaultExceptions


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

    # ------------------------------------------------------------------------------------------------------
    def append(self, other: dict[str, str, str]):
        date, subj, text = other['date'], other['subj'], other['text']
        self.__vault.setdefault(date, []).append((subj, text))

    def _get(self, date: str) -> list:
        return self.__vault.get(date, [])

    def _pop(self, date: str) -> list:
        return self.__vault.pop(date, [])

    def delete(self, date: str, iex: int):
        value = self.__vault[date].pop(iex)
        if len(self.__vault[date]) == 0:
            self.__vault.pop(date, [])
        return value
    # ------------------------------------------------------------------------------------------------------

    def get_coming_days(self, dates_arr: set) -> set:
        dates = set(self.__vault.keys())
        return dates & dates_arr

    def date_exist(self, date: str) -> bool:
        return date in self.__vault.keys()

    # ------------------------------------------------------------------------------------------------------

    def request(self, date: str, forced: int = 0) -> list:
        """
        :param date: string date key with format dd.mm.yy
        :param forced: 0 - news will delete, 1 - stay in vault
        :return: news list
        """
        if not self.date_exist(date):
            error_text = "Value ({0}) not found. Function request({1})"
            req_func = ('pop', 'get')[forced]
            raise VaultExceptions(error_text.format(date, req_func))
        return self._get(date) if forced else self._pop(date)

    def garbage_collector(self, cur_date: str) -> list:
        deleted_dates = []
        for date in self.__vault.keys():
            if date_comparison(cur_date, date) > 0:
                self._pop(date)
                deleted_dates.append(date)

        return deleted_dates
