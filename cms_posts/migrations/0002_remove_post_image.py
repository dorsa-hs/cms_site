# Generated by Django 3.2.6 on 2021-09-13 09:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms_posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='image',
        ),
    ]
