from datetime import date as dt

from django.db.models import Q

from .import models

def getDayOfWeek(ojo):
    if ojo != None:
        str_date = str(ojo)
        format_date = dt.fromisoformat(str_date)
        return str(format_date.weekday())

def get_available_venues(start,end,date_day):
    keys = []
    qday = getDayOfWeek(date_day)
    day = models.SummaryTimetable.objects.filter(Q(start_date=date_day)|Q(day=qday))
    equal = day.filter(Q(start_time=start))
    obj =  day.filter(~Q(start_time=start))
    between = obj.filter((Q(start_time__lt=start) & Q(end_time__gt=start))|(Q(start_time__gt=start) & Q(start_time__lt=end)))
    final = between.union(equal)

    for item in final:
        keys.append(item.venue)
    
    available = models.Venue.objects.exclude(id__in=keys)

    return available