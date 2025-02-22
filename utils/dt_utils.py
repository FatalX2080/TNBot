from datetime import datetime, time, timedelta


#sbt = (time(*LEFT_BORDER), time(*RIGHT_BORDER))
date_format = '%d.%m.%y'


def get_date():
    return format_date(datetime.now().date())


def format_date(date):
    return date.strftime(date_format)


def get_time():
    return datetime.now().time()


def check_send_time():
    return sbt[0] <= get_time() <= sbt[1]


def now():
    return datetime.now()


def days_delta(date):
    return timedelta(days=date)


def check_date(date):
    day, month, year = date.split('.')
    year_len = len(year)
    if (int(day) > 31) or (int(month) > 12) or (year_len != 2 and year_len != 4):
        return 1
    date_formating = '%d.%m.%' + ('Y' if not year_len % 4 else 'y')
    date = datetime.strptime(date, date_formating)

    return 1 if date < now() else 0
