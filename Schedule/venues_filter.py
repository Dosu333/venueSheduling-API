from datetime import timedelta, time, datetime 
from datetime import date as dt
from pytz import UTC as u


from .import models

def is_between(time, time_range):
    if time_range[1] < time_range[0]:
        return time > time_range[0] or time < time_range[1]
    return time_range[0] < time < time_range[1]

def getDayOfWeek(ojo):
    if ojo != None:
        str_date = str(ojo)
        format_date = dt.fromisoformat(str_date)
        return str(format_date.weekday())

def get_available_venues(start,end,date=None,day=None):
    venue_on_day = []
    venue_not_on_day = []
    show_venues = []
    ven_no = []
    displace = []
    unique =[]
    events = []
    keys ={}

    if date is not None:
        qday = getDayOfWeek(date)

        for item in models.SchoolTimetable.objects.all():
            """Adds school timetables on the same day as date received and those not to respective list""" 

            if item.day == qday:
                venue_on_day.append(item)
            else:
                venue_not_on_day.append(item)

        for item in models.UserScheduledTimetable.objects.all():
            """Adds user scheduled timetables on the same date as date received and those not respective list""" 
            if item.start_date_and_time.date() == date:
                venue_on_day.append(item)
            else:
                venue_not_on_day.append(item)

        for item in models.ExamTimetable.objects.all():
            """Adds exam timetables on the same as date received and those not to respective list""" 
            if item.start_date_and_time.date() == date:
                venue_on_day.append(item)
            else:
                venue_not_on_day.append(item)
        
        for item in models.Event.objects.all():
            """Adds events on the same date as date received to events list""" 
            if item.start_date_and_time.date() == date:
                events.append(item)
            
        
    if day is not None:
        for item in models.SchoolTimetable.objects.all():
            """Adds school timetables on the same day as date received and those not to respective list""" 
            if item.day == day:
                venue_on_day.append(item)
            else:
                venue_not_on_day.append(item)

        for item in models.UserScheduledTimetable.objects.all():
            """Adds user scheduled timetables on the same day as day received and those not respective list""" 
            if getDayOfWeek(item.start_date_and_time.date()) == day:
                venue_on_day.append(item)
            else:
                venue_not_on_day.append(item)

        for item in models.ExamTimetable.objects.all():
            """Adds exam timetables on the same day as day received and those not to respective list"""
            if getDayOfWeek(item.start_date_and_time.date()) == day:
                venue_on_day.append(item)
            else:
                venue_not_on_day.append(item)

        for item in models.Event.objects.all():
            """Adds events on the same day as day received to events list""" 
            if getDayOfWeek(item.start_date_and_time.date()) == day:
                events.append(item)
    
    for items in venue_on_day:
        """Puts objects that doesn't have the same starting time as received starting in a list of objects to show """ 
        try:
            if items.start_time != start:
                show_venues.append(items)
            elif items.start_time == start:
                ven_no.append(items)
        except AttributeError:
            if items.start_date_and_time.time() != start:
                show_venues.append(items)
            elif items.start_date_and_time.time() == start:
                ven_no.append(items)


    for item in show_venues:
        """Checks for objects whose times intersect with received times and puts them in a list of objects not to show"""
        try:
            if is_between(start, (item.start_time, item.end_time)) or is_between(item.start_time,(start,end)):
                ven_no.append(item)
        except AttributeError:
            if is_between(start, (item.start_date_and_time.time(), item.end_time)) or is_between(item.start_date_and_time.time(),(start,end)):
                ven_no.append(item)

    for obj in show_venues:
        """Compares the list of venues to show with the list of venues not to show and puts objects with the same venue in a list"""
        for ven in ven_no:
            if obj.venue == ven.venue:
                displace.append(obj)

    for obj in venue_not_on_day:
        """Gets venues that have no instance on the day or date received"""
        for ven in venue_on_day:
            if obj.venue == ven.venue:
                unique.append(obj)

    for objects in displace:
        """Removes objects from venues to show with the same venue as objects in the list of venues not to sho w"""
        if objects in show_venues:
            show_venues.remove(objects)

    displace.clear()

    for items in venue_not_on_day:
        """Adds venues with no instance on the date received to the list of venues to show"""
        if items not in unique:
            show_venues.append(items)

    unique.clear()
    
    for item in events:
        """Checks if 2hrs after an event has ended the starting time received will not have begun"""
        end_time = (datetime.combine(dt(1,1,1), item.end_time) + timedelta(hours=2)).time()
        if start < end_time or end_time >= time(7,00):
            displace.append(item)

    for item in show_venues:
        """Compares the list of venues with events with the list of venues show and puts objects with the same venue in a list"""
        for obj in displace:
            if item.venue == obj.venue:
                unique.append(item)

    for item in unique:
        """Removes objects that have events taking place in them and won't be free at the starting time received"""
        if item in show_venues:
            show_venues.remove(item)
            
    for item in show_venues:
        if item.venue.id in keys:
            continue
        keys[str(item.venue.id)] = item.venue.name

    return keys


def re_check_venues(start,end,venue,date):
    avail_ven = get_available_venues(start,end,date)
    if venue in avail_ven:
        return True
    return False
    
        