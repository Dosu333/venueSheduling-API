# Generated by Django 3.1.2 on 2020-10-07 12:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0010_auto_20201007_0748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='department',
        ),
    ]