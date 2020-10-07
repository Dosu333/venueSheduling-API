from datetime import timedelta, time, datetime 
from datetime import date as dt
from pytz import UTC as u

from .helper_functions import is_between, getDayOfWeek, events


from .import models

def get_available_venues(start,end,date_day):
    venue_not_on_day = []
    show_venues = []
    ven_no = []
    displace = []
    unique =[]
    keys ={}

    for items in models.SummaryTimetable.objects.all():
        """Puts objects that doesn't have the same starting time as received starting in a list of objects to show """ 
        try:
            qday = getDayOfWeek(date_day)
            if items.start_time != start and items.day == qday:
                show_venues.append(items)
            elif items.day != qday:
                venue_not_on_day.append(items)
            elif items.start_time == start:
                ven_no.append(items)
        except AttributeError:
            if items.start_date_and_time.time() != start and getDayOfWeek(items.start_date_and_time.date()) == date_day:
                show_venues.append(items)
            elif getDayOfWeek(items.start_date_and_time.date()) != date_day:
                venue_not_on_day.append(items)
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

    d = show_venues + ven_no

    for obj in venue_not_on_day:
        """Gets venues that have no instance on the day or date received"""
        for ven in d:
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
    
    for item in events(date_day):
        """Checks if 2hrs after an event has ended the starting time received will not have begun"""
        end_time = (datetime.combine(dt(1,1,1), item.end_time) + timedelta(hours=2)).time()
        if start < end_time or end_time >= time(7,00):
            displace.append(item)

    for item in show_venues:
        """Compares the list of venues with events with the list of venues show and puts objects with the same venue in a list"""
        for obj in displace:
            if item.venue == obj.venue.id:
                unique.append(item)

    for item in unique:
        """Removes objects that have events taking place in them and won't be free at the starting time received"""
        if item in show_venues:
            show_venues.remove(item)
            
    for item in show_venues:
        if str(item.venue) in keys:
            continue
        available = models.Venue.objects.get(pk=item.venue)
        keys[str(item.venue)] = (available.name, available.capacity) 

    return keys