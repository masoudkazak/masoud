# Generated by Django 3.2.9 on 2022-02-10 08:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0015_alter_address_mobile_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='mobile_number',
            field=models.CharField(max_length=20, validators=[django.core.validators.RegexValidator(message='شماره وارد شده اشتباه است\n09123456789', regex='^(\\+98|0)?9\\d{9}$')]),
        ),
    ]
