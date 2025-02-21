from . import event


class Dispatcher:
    def __init__(self):
        self.__news_dict = {}

    def user_exist(self, uid: int):
        return uid in self.__news_dict.keys()

    def create_news(self, user: int):
        if self.user_exist(user):
            return
        self.__news_dict[user] = event.Event()

    def add_info(self, user: int, stage: int, info:str):
        if not self.user_exist(user):
            return

        match stage:
            case 1:
                self.__news_dict[user].set_date(info)
            case 2:
                self.__news_dict[user].set_subject(info)
            case 3:
                self.__news_dict[user].set_text(info)
            case _:
                raise Exception