# Generated by Django 3.1.2 on 2020-10-15 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Schedule', '0013_auto_20201012_1457'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='is_conference_hall',
            field=models.BooleanField(default=False),
        ),
    ]