# Generated by Django 2.0.2 on 2018-04-22 12:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_allrequest'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='plan_defect',
        ),
    ]
