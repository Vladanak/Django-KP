# Generated by Django 2.0.2 on 2018-04-22 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0017_post_plan_defect'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='plan_defect',
            field=models.BigIntegerField(blank=True, default='0', null=True),
        ),
    ]
