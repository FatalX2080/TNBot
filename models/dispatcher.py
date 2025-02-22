from . import event


class Dispatcher:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.__news_dict = {}

    def get(self, uid: int):
        return self.__news_dict.get(uid, None)

    def pop(self, uid: int):
        return self.__news_dict.pop(uid, None)

    def check_for_exist(self, uid: int):
        return uid in self.__news_dict.keys()

    def create_news(self, user: int):
        if self.check_for_exist(user):
            return
        self.__news_dict[user] = event.Event()

    def add_info(self, user: int, stage: int, info: str):
        if not self.check_for_exist(user):
            raise Exception("User {0} not exist in {1}".format(user, self.check_for_exist))

        match stage:
            case 1:
                self.__news_dict[user].set_date(info)
            case 2:
                self.__news_dict[user].set_subject(info)
            case 3:
                self.__news_dict[user].set_text(info)
            case _:
                raise Exception
