from django.contrib import admin

from .import models
# Register your models here.
admin.site.register(models.Course)
admin.site.register(models.SchoolTimetable)
admin.site.register(models.ExamTimetable)
admin.site.register(models.UserScheduledTimetable)
admin.site.register(models.Venue)
admin.site.register(models.Event)
admin.site.register(models.Notification)
admin.site.register(models.SummaryTimetable)