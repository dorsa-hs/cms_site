# Generated by Django 3.2.6 on 2021-09-01 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms_category', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='postcategory',
            name='on_home',
            field=models.BooleanField(default=False, verbose_name='نمایش دسته در خانه'),
        ),
    ]
