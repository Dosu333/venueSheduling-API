from datetime import date as dt

from django.db.models import Q

from .models import Venue, SummaryTimetable as queryset

def getDayOfWeek(ojo):
    if ojo != None:
        str_date = str(ojo)
        format_date = dt.fromisoformat(str_date)
        return str(format_date.weekday())

def get_available_venues(start,end,date_day,content_type=None,all_venues=True,table=queryset.objects.all()):
    keys = []
    if content_type is not None:
        table = table.filter(content_type=content_type)
    try:
        qday = getDayOfWeek(date_day)
        on_day = table.filter(Q(start_date=date_day)|Q(day=qday))
    except:
        on_day = table.filter(Q(day=date_day))
        
    equal = on_day.filter(Q(start_time=start))
    not_equal =  on_day.filter(~Q(start_time=start))
    between = not_equal.filter((Q(start_time__lt=start) & Q(end_time__gt=start))|(Q(start_time__gt=start) & Q(start_time__lt=end)))
    final = between.union(equal)

    for item in final:
        keys.append(item.venue)

    available = Venue.objects.exclude(id__in=keys)

    if all_venues:
        return available
    return available.exclude(is_conference_hall=True)