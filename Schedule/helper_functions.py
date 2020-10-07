from datetime import timedelta, time, datetime 
from datetime import date as dt

from.models import Event
def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time > time_range[0] or time < time_range[1]
    return time_range[0] < time < time_range[1]

def getDayOfWeek(ojo):
    if ojo != None:
        str_date = str(ojo)
        format_date = dt.fromisoformat(str_date)
        return str(format_date.weekday())

def events(d):
    ev = []
    for items in Event.objects.all():
        try:
            if items.start_date_and_time.date() == d:
                ev.append(items)
        except AttributeError:
            if getDayOfWeek(items.start_date_and_time.date()) == d:
                ev.append(items)
    return ev