from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from accounts.models import Department

import uuid
# Create your models here.
class SummaryTimetable(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    DAY_CHOICES = [
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5','Saturday')
    ]
    day = models.CharField(max_length=10, choices=DAY_CHOICES, null=True,blank=True)
    start_date = models.DateField(null=True, blank=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time =  models.TimeField()
    venue = models.UUIDField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.UUIDField()
    content_object = GenericForeignKey()

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venue = models.ForeignKey('Venue', on_delete=models.SET_NULL, null=True,)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    end_time = models.TimeField()

class Course(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    code = models.CharField(max_length=6, unique=True)
    title = models.CharField(max_length=150)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
     return self.code

class SchoolTimetable(BaseModel): 
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=150, null=True, blank=True)
    venue = models.ForeignKey('Venue', on_delete=models.CASCADE, null=True)
    start_date_and_time = models.DateTimeField()
    end_time = models.TimeField()
    PURPOSE_CHOICES = [
        ('Lecture','Lecture'),
        ('Defence','Defence'),
        ('Meeting','Meeting'),
        ('Test','Test'),
    ]
    purpose = models.CharField(max_length=7, choices=PURPOSE_CHOICES)
    
    def __str__(self):
        return self.venue.name

class Venue(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150, unique=True)
    capacity = models.IntegerField(null=True)
    is_conference_hall = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name, self.capacity)

class ExamTimetable(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True)
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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=150, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
