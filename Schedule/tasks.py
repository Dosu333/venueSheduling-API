from celery import shared_task
 
from django.db.models import Q

from datetime import datetime

from.models import SummaryTimetable

@shared_task
def clean_tables():
    today = datetime.today()
    now = datetime.now().time()
    qs = SummaryTimetable.objects.filter(Q(start_date__lt=today) | (Q(start_date=today) & Q(end_time__lte=now)) )

    for items in qs:
        items.content_object.delete()
        items.delete()