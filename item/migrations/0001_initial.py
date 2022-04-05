# Generated by Django 3.2.9 on 2022-04-05 07:52

import ckeditor.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_jalali.db.models
import taggit.managers


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('taggit', '0003_taggeditem_add_unique_index'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='نام')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='ColorItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=100, verbose_name='رنگ')),
            ],
            options={
                'verbose_name': 'رنگ',
                'verbose_name_plural': 'رنگ ها',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='نام محصول')),
                ('price', models.BigIntegerField(verbose_name='قیمت')),
                ('body', ckeditor.fields.RichTextField(verbose_name='نوضیحات')),
                ('date', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ')),
                ('updated', django_jalali.db.models.jDateTimeField(auto_now=True, verbose_name='تاریخ آخرین تغییر')),
                ('inventory', models.PositiveIntegerField(default=0, verbose_name='موجودی')),
                ('discount', models.FloatField(blank=True, null=True, verbose_name='درصد تخفیف')),
                ('status', models.CharField(choices=[('p', 'منتشر'), ('d', 'پیش نویس')], default='d', max_length=10, verbose_name='وضعيت')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='item.category', verbose_name='دسته بندی')),
                ('color', models.ManyToManyField(to='item.ColorItem', verbose_name='رنگ ها')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='فروشنده')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Uploadimage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='uploads/%Y/%m/%d/', verbose_name='عکس')),
                ('item_id', models.CharField(blank=True, max_length=10, null=True, verbose_name='آیدی محصول')),
            ],
            options={
                'verbose_name': 'تصویر محصول',
                'verbose_name_plural': 'تصویر محصولات',
            },
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(default=1, verbose_name='تعداد')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='مشتری')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.item', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'سفارش محصول',
                'verbose_name_plural': 'سفارش محصولات',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ')),
                ('items', models.ManyToManyField(to='item.OrderItem', verbose_name='محصولات')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL, verbose_name='مشتری')),
            ],
            options={
                'verbose_name': 'سبد مشتری',
                'verbose_name_plural': 'سبد مشتری ها',
            },
        ),
        migrations.AddField(
            model_name='item',
            name='images',
            field=models.ManyToManyField(blank=True, to='item.Uploadimage', verbose_name='عکس ها'),
        ),
        migrations.AddField(
            model_name='item',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='تگ ها'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', ckeditor.fields.RichTextField(verbose_name='متن')),
                ('date', django_jalali.db.models.jDateTimeField(auto_now_add=True, verbose_name='تاریخ')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='item.item', verbose_name='محصول')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'کامنت',
                'verbose_name_plural': 'نظرها',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip_code', models.CharField(max_length=250, verbose_name='کد تلفن')),
                ('home_address', models.TextField(verbose_name='آدرس')),
                ('mobile_number', models.CharField(max_length=13, validators=[django.core.validators.RegexValidator(message='شماره وارد شده اشتباه است\n09123456789', regex='^(\\+98|0)?9\\d{9}$')], verbose_name='شماره موبایل')),
                ('body', models.TextField(blank=True, null=True, verbose_name='توضیحات')),
                ('this_address', models.BooleanField(default=False, verbose_name='آدرس فعال')),
                ('province', models.CharField(default='تهران', max_length=100, verbose_name='استان')),
                ('city', models.CharField(default='تهران', max_length=100, verbose_name='شهر')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address_user', to=settings.AUTH_USER_MODEL, verbose_name='مشتری')),
            ],
            options={
                'verbose_name': 'آدرس',
                'verbose_name_plural': 'آدرس ها',
            },
        ),
    ]
