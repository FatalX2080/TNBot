from datetime import datetime, time, timedelta
from config import DATE_FORMAT


def get_date():
    return date_to_str(datetime.now().date())


def date_to_str(date) -> str:
    return date.strftime(DATE_FORMAT)


def str_to_date(date: str):
    return datetime.strptime(date, DATE_FORMAT)


def get_time() -> time:
    return datetime.now().time()


def tuple_to_time(t: tuple) -> time:
    return time(*t)


def check_send_time(borders):
    b = (
        tuple_to_time(borders[0]),
        tuple_to_time(borders[1])
    )
    return b[0] <= get_time() <= b[1]


def now():
    return datetime.now()


def days_delta(date: float | int) -> timedelta:
    return timedelta(days=date)


def check_date(date):
    ln = len(date.split('.'))
    if ln == 2:
        date += '.' + get_year()
    day, month, year = date.split('.')
    year_len = len(year)
    if (int(day) > 31) or (int(month) > 12) or (year_len != 2 and year_len != 4):
        return 1
    date_formating = '%d.%m.%' + ('Y' if not year_len % 4 else 'y')
    date = datetime.strptime(date, date_formating).date()
    return 1 if date < now().date() else 0


def week_day(date: str) -> int:
    date = str_to_date(date)
    return date.weekday()


def poll_date_calculating(day_id: int) -> str:
    dt_now = datetime.now()
    cur_day = dt_now.weekday()
    delta = 6 - cur_day + day_id + 1 if cur_day >= day_id else day_id - cur_day
    date = dt_now + days_delta(delta)
    return date_to_str(date.date())


def date_comparison(a: str, b: str) -> int:
    # 01.23.45 -> 452301
    dt1 = dt_comp_prepare(a)
    dt2 = dt_comp_prepare(b)
    if dt1 < dt2:
        return 1
    if dt1 > dt2:
        return -1
    return 0


def dt_comp_prepare(a: str):
    return a[4], a[5], a[2], a[3], a[0], a[1]


def get_year() -> str:
    return str(datetime.now().year)
