# Generated by Django 3.2.9 on 2022-05-12 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_companyprofile_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprofile',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='درمورد شرکت'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(blank=True, null=True, verbose_name='درمورد من'),
        ),
    ]
