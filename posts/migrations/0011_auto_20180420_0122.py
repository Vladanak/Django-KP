# Generated by Django 2.0.2 on 2018-04-19 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_post_plan_all'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='plan_clock_all',
            field=models.BigIntegerField(default='0'),
        ),
        migrations.AddField(
            model_name='post',
            name='plan_rez_all',
            field=models.BigIntegerField(default='0'),
        ),
    ]