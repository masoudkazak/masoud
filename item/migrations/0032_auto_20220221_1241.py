# Generated by Django 3.2.9 on 2022-02-21 09:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('item', '0031_alter_address_mobile_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.CharField(choices=[('p', 'Published'), ('d', 'Draft')], default='d', max_length=10),
        ),
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address_user', to=settings.AUTH_USER_MODEL, verbose_name='مشتری'),
        ),
    ]