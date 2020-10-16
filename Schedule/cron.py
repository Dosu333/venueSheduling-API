from Schedule.models import SummaryTimetable

from datetime import datetime

from django.db.models import Q

def clean_tables():
    today = datetime.today().strftime('%Y-%m-%d')
    now = datetime.utcnow().time()
    qs = SummaryTimetable.objects.filter(start_date=today)
    clean = qs.filter(Q(end_time=now)|Q(end_time__lt=now))

    for items in clean:
        items.content_object.delete()
        items.delete()