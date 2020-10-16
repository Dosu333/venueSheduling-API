from datetime import date as dt

from django.db.models import Q
from django.contrib.contenttypes.models import ContentType

from .models import Venue, Notification, UserScheduledTimetable, SummaryTimetable as queryset

def getDayOfWeek(ojo):
    if ojo != None:
        str_date = str(ojo)
        format_date = dt.fromisoformat(str_date)
        return str(format_date.weekday())

def get_available_venues(start,end,date_day,content_type=None,all_venues=True,notify=False,table=queryset.objects.all()):
    keys = []
    if content_type is not None:
        table = table.filter(content_type=content_type)
    try:
        qday = getDayOfWeek(date_day)
        on_day = table.filter(Q(start_date=date_day)|Q(day=qday))
    except:
        if notify:
            qday = int(date_day) + 1
            on_day = table.filter(start_date__iso_week_day=qday)
        else:
            on_day = table.filter(day=date_day)
    
    equal = on_day.filter(start_time=start)
    not_equal =  on_day.filter(~Q(start_time=start))
    between = not_equal.filter((Q(start_time__lt=start) & Q(end_time__gt=start))|(Q(start_time__gt=start) & Q(start_time__lt=end)))
    final = between.union(equal)

    for item in final:
        keys.append(item.venue)

    available = Venue.objects.exclude(id__in=keys)

    if all_venues:
        return available
    elif notify:
        return (equal,between)
    return available.exclude(is_conference_hall=True)

def send_notifications(start,end,date_day,venue):
    obj_type =  ContentType.objects.get(app_label='Schedule',model='userscheduledtimetable')
    clashes = get_available_venues(start=start,end=end,date_day=date_day,content_type=obj_type,notify=True,all_venues=False)
    t = clashes[0].filter(venue=venue)
    btw = clashes[1].filter(venue=venue)
    cl = btw.union(t)

    for item in cl:
        user_obj = UserScheduledTimetable.objects.get(id=item.object_id)
        summary = queryset.objects.get(content_type=obj_type,object_id=item.object_id)
        msg = """ 
               Your scheduling of the venue {} for a {} on {} has ben revoked.
               The school wants to make use of it and your time of usage clashes with that of the school.
               Try resheduling for another venue or scheduling another time.
               We're sorry for any inconviniences.
              """
        Notification.objects.create(user=user_obj.user, title="Venue Revoked", text=msg.format(user_obj.venue.name,user_obj.purpose,item.start_date))
        user_obj.delete()
        summary.delete()