# Generated by Django 3.2.6 on 2021-09-13 09:29

import cms_posts.models
from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('cms_posts', '0004_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format=None, keep_meta=True, null=True, quality=90, size=[730, 730], upload_to=cms_posts.models.upload_image_path, verbose_name='تصویر'),
        ),
    ]
