# Generated by Django 3.1.2 on 2020-10-07 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20201006_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]