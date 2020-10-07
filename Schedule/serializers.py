from rest_framework import serializers

from . import models
from .venues_filter import get_available_venues

from datetime import datetime, time, date
from pytz import UTC as utc

def check_time_within_working_hours(start,end):
    return (start >= time(7,00) and start <= time(18,30)) and (end >= time(8,00) and end <= time(19,00))


class BaseSerializer(serializers.ModelSerializer):


    def validate(self,attrs):
        start_date_and_time = attrs.get('start_date_and_time')
        end_time = attrs.get('end_time')
        today_date = utc.localize(datetime.now())

        if today_date > start_date_and_time.replace(tzinfo=utc):
            msg = "Enter a future date and time"
            raise serializers.ValidationError(msg)

        if start_date_and_time.date().weekday() == 6:
            raise serializers.ValidationError("Working days are from Monday to Saturday")

        if end_time <= start_date_and_time.time():
            raise serializers.ValidationError("The end must occur after start")

        if not check_time_within_working_hours(start=start_date_and_time.time(), end=end_time):
            raise serializers.ValidationError("Time must be within working hours")
        
        return attrs


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Course
        fields = ('__all__')
        read_only_fields = ['id','users' ]

class VenueSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Venue
        fields = ('__all__')
        read_only_fields = ['id', ]

class ExamTimetableSerializer(BaseSerializer):

    class Meta:
        model = models.ExamTimetable
        fields = ('id','course','venue','users','start_date_and_time','end_time')
        read_only_fields = ['id', 'users']


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Event
        fields = ('__all__')
        read_only_fields = ['id', 'users']

class UserScheduledTimetableSerializer(serializers.ModelSerializer):
    start_date_and_time = serializers.DateTimeField(format=None)
    end_time = serializers.TimeField(format=None)
    
    class Meta:
        model = models.UserScheduledTimetable
        fields = ('__all__')
        read_only_fields = ['id', 'user']

    def validate(self, attrs):
        start = attrs.get('start_date_and_time').time()
        end = attrs.get('end_time')
        date = attrs.get('start_date_and_time').date()
        date_time = attrs.get('start_date_and_time')
        venue = attrs.get('venue')
        today_date = utc.localize(datetime.now())

        if today_date > date_time.replace(tzinfo=utc):
            msg = "Enter a future date and time"
            raise serializers.ValidationError(msg)

        if date.weekday() == 6:
            raise serializers.ValidationError("Working days are from Monday to Saturday")

        if end <= start:
            raise serializers.ValidationError("The end must occur after start")

        if not check_time_within_working_hours(start=start, end=end):
            raise serializers.ValidationError("Time must be within working hours")


        avail_ven = get_available_venues(start=start,end=end,date_day=date)
        if str(venue.id) not in avail_ven:
            raise serializers.ValidationError("Venue no longer available")
        
        return attrs


class SchoolTimetableSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SchoolTimetable
        fields = ('id','course','day','start_time','end_time','venue','users')
        read_only_fields = ['id', 'users']

    
    def validate(self,data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')

        if end_time <= start_time:
            raise serializers.ValidationError("The end time must occur after start time")

        if not check_time_within_working_hours(start=start_time, end=end_time):
            raise serializers.ValidationError("Time must be within working hours")

        return data

class QueryParamsSerializer(BaseSerializer):
    start_date_and_time = serializers.DateTimeField(format=None)
    end_time = serializers.TimeField(format=None)

    class Meta:
        model = models.UserScheduledTimetable
        fields = ('start_date_and_time','end_time')

class NotificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Notification
        fields = ('__all__')
        read_only_fields = ['id','created_at']

class UserScheduledDetailSerializer(serializers.ModelSerializer):
    course = serializers.StringRelatedField()
    venue = serializers.StringRelatedField()
    
    class Meta:
        model  = models.UserScheduledTimetable
        fields = ('__all__')
        read_only_fields = ['__all__']