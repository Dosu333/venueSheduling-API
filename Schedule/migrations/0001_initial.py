# Generated by Django 3.1.2 on 2020-11-04 13:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('end_time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('code', models.CharField(max_length=6, unique=True)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=150, null=True)),
                ('text', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SummaryTimetable',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('day', models.CharField(blank=True, choices=[('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday')], max_length=10, null=True)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('start_time', models.TimeField(blank=True, null=True)),
                ('end_time', models.TimeField()),
                ('venue', models.UUIDField()),
                ('object_id', models.UUIDField()),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150, unique=True)),
                ('capacity', models.IntegerField(null=True)),
                ('is_conference_hall', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Schedule.basemodel')),
                ('name', models.CharField(max_length=150)),
                ('start_date_and_time', models.DateTimeField()),
            ],
            bases=('Schedule.basemodel',),
        ),
        migrations.CreateModel(
            name='ExamTimetable',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Schedule.basemodel')),
                ('start_date_and_time', models.DateTimeField()),
            ],
            bases=('Schedule.basemodel',),
        ),
        migrations.CreateModel(
            name='SchoolTimetable',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Schedule.basemodel')),
                ('day', models.CharField(choices=[('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'), ('4', 'Friday'), ('5', 'Saturday')], max_length=10)),
                ('start_time', models.TimeField()),
            ],
            bases=('Schedule.basemodel',),
        ),
        migrations.CreateModel(
            name='UserScheduledTimetable',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=150, null=True)),
                ('start_date_and_time', models.DateTimeField()),
                ('end_time', models.TimeField()),
                ('purpose', models.CharField(choices=[('Lecture', 'Lecture'), ('Defence', 'Defence'), ('Meeting', 'Meeting'), ('Test', 'Test')], max_length=7)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Schedule.course')),
            ],
        ),
    ]