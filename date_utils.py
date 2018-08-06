import time
from datetime import datetime
from datetime import timedelta
from datetime import date

def get_timestamp_day_start(offest_days=0):
    now = datetime.now()
    datetime_start = datetime(now.year, now.month, now.day, 0, 0, 0)

    if offest_days > 0:
        datetime_start += timedelta(days=offest_days)
    else:
        datetime_start -= timedelta(days=(offest_days * -1))

    return get_timestamp_from_datetime(datetime_start)

def get_timestamp_day_end(offest_days=0):
    now = datetime.now()
    datetime_end = datetime(now.year, now.month, now.day, 23, 59, 59)

    if offest_days > 0:
        datetime_end += timedelta(days=offest_days)
    else:
        datetime_end -= timedelta(days=(offest_days * -1))

    return get_timestamp_from_datetime(datetime_end)

def get_timestamp_from_datetime(dt):
    return int((dt - datetime(1970, 1, 1)).total_seconds())

def get_day_number(dt):
    beginning_of_year = date(dt.year, 1, 1)
    delta = dt.date() - beginning_of_year
    return delta.days + 1

def get_start_end_from_args(args):
    offset_start_day = int((len(args) > 1 and args[1]) or 0)
    offset_end_day = int((len(args) > 2 and args[2]) or 0)

    start_sec = get_timestamp_day_start(offset_start_day);
    end_sec = get_timestamp_day_end(offset_end_day);

    return start_sec, end_sec
