# Generated by Django 2.0.2 on 2018-04-14 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_post_plan_rez'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='plan_clock',
            field=models.BigIntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='post',
            name='plan_clock_rez',
            field=models.BigIntegerField(default='0'),
        ),
    ]
