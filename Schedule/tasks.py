from celery import shared_task

from django.db.models import Q

from datetime import datetime

from.models import SummaryTimetable

@shared_task
def clean_tables():
    today = datetime.today().strftime('%Y-%m-%d')
    now = datetime.now().time()
    qs = SummaryTimetable.objects.filter(start_date=today)
    clean = qs.filter(Q(end_time=now)|Q(end_time__lt=now))

    for items in clean:
        items.content_object.delete()
        items.delete()