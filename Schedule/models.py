from django.db import models
from django.conf import settings

from accounts.models import Department

import uuid
# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venue = models.ForeignKey('Venue', on_delete=models.SET_NULL, null=True, blank=True)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    end_time = models.TimeField()

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    code = models.CharField(max_length=6, unique=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
     return self.code

class SchoolTimetable(BaseModel): 
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    DAY_CHOICES = [
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5','Saturday')
    ]
    day = models.CharField(max_length=10, choices=DAY_CHOICES)
    start_time = models.TimeField()

    def __str__(self):
        return self.course.code

    
    
    
class UserScheduledTimetable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE, null=True, blank=True)
    start_date_and_time = models.DateTimeField()
    end_time = models.TimeField()
    PURPOSE_CHOICES = [
        ('LT','Lecture'),
        ('DF','Defence'),
        ('MT','Meeting'),
        ('TS','Test'),
    ]
    purpose = models.CharField(max_length=7, choices=PURPOSE_CHOICES)

    def __str__(self):
        return self.venue.name


class Venue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)
    capacity = models.IntegerField(null=True)

    def __str__(self):
        return "{}---{}".format(self.name, self.capacity)


class ExamTimetable(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    start_date_and_time = models.DateTimeField()

    def __str__(self):
        return self.course.code
        
class Event(BaseModel):
    name = models.CharField(max_length=150)
    start_date_and_time = models.DateTimeField()

    def __str__(self):
        return self.name

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=150, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)