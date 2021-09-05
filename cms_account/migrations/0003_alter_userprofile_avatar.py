# Generated by Django 3.2.6 on 2021-09-04 20:45

import cms_account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_account', '0002_alter_userprofile_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='avatar',
            field=models.ImageField(blank=True, default='default_profile_pic', null=True, upload_to=cms_account.models.upload_image_path, verbose_name='آواتار'),
        ),
    ]
