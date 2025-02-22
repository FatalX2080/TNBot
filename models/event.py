class Event:
    def __init__(self):
        self._date = ""
        self._subject = ""
        self._text = ""

    def set_date(self, date: str):
        self._date = date

    def set_subject(self, suj: str):
        self._subject = suj

    def set_text(self, text: str):
        self._text = text

    def info(self) -> tuple[str, str, str]:
        return self._date, self._subject, self._text
