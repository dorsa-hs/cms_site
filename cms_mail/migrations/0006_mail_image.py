# Generated by Django 3.2.6 on 2021-09-29 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_mail', '0005_remove_mail_send_now'),
    ]

    operations = [
        migrations.AddField(
            model_name='mail',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='عکس(اختیاری)'),
        ),
    ]
