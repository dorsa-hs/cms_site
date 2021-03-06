# Generated by Django 3.2.6 on 2021-09-11 18:57

import ckeditor_uploader.fields
import cms_posts.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_jalali.db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200, unique=True, verbose_name='عنوان')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='عنوان در url')),
                ('created_on', django_jalali.db.models.jDateField(verbose_name='تاریخ')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='محتوا')),
                ('active', models.BooleanField(default=False, verbose_name='فعال / غیرفعال')),
                ('image', models.ImageField(blank=True, null=True, upload_to=cms_posts.models.upload_image_path, verbose_name='تصویر')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده')),
            ],
            options={
                'verbose_name': 'پست',
                'verbose_name_plural': 'پست ها',
                'ordering': ['-created_on'],
            },
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='عنوان')),
                ('name', models.CharField(max_length=150, verbose_name='عنوان در URL')),
                ('on_home', models.BooleanField(default=False, verbose_name='نمایش دسته در خانه')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی ها',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120, verbose_name='عنوان')),
                ('slug', models.SlugField(verbose_name='عنوان در url')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')),
                ('active', models.BooleanField(default=True, verbose_name='فعال / غیر فعال')),
                ('posts', models.ManyToManyField(blank=True, to='cms_posts.Post', verbose_name='پست ها')),
            ],
            options={
                'verbose_name': 'برچسب / تگ',
                'verbose_name_plural': 'برچسب ها / تگ ها',
            },
        ),
        migrations.AddField(
            model_name='post',
            name='categories',
            field=models.ManyToManyField(blank=True, to='cms_posts.PostCategory', verbose_name='دسته بندی ها'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='محتوا')),
                ('date_posted', django_jalali.db.models.jDateField(default=django.utils.timezone.now, verbose_name='تاریخ')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='نویسنده نظر')),
                ('blogpost_connected', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='cms_posts.post', verbose_name='پست')),
            ],
            options={
                'verbose_name': 'نظر',
                'verbose_name_plural': 'نظرات',
            },
        ),
    ]
