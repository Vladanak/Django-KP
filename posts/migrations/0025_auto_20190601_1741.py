# Generated by Django 2.2.1 on 2019-06-01 17:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0024_auto_20190601_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='specialty',
            field=models.CharField(default=True, max_length=50, validators=[django.core.validators.RegexValidator(code='invalid_regex', message='Only alphanumeric characters are allowed.', regex='[^\\W\\d_]+$')]),
        ),
        migrations.AlterField(
            model_name='post',
            name='text',
            field=models.CharField(max_length=100, validators=[django.core.validators.RegexValidator(code='invalid_regex', message='Only alphanumeric characters are allowed.', regex='[^\\W\\d_]+$')]),
        ),
    ]
