# Generated by Django 3.2.6 on 2021-09-17 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cms_contact', '0002_newslettersignup'),
        ('cms_mail', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=989, verbose_name='موضوع پیام')),
                ('message', models.TextField(blank=True, verbose_name='متن پیام')),
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('last_updated', models.DateTimeField(auto_now=True, db_index=True)),
                ('status', models.PositiveSmallIntegerField(blank=True, choices=[(0, 'sent'), (1, 'failed'), (2, 'queued')], db_index=True, null=True, verbose_name='Status')),
                ('send_now', models.BooleanField(default=False, verbose_name='ارسال همین حالا')),
                ('mail_service', models.ForeignKey(max_length=254, on_delete=django.db.models.deletion.CASCADE, to='cms_mail.mailsetting', verbose_name='سرویس mail')),
                ('to', models.ForeignKey(max_length=254, on_delete=django.db.models.deletion.CASCADE, to='cms_contact.newslettersignup', verbose_name='ارسال به')),
            ],
            options={
                'verbose_name': 'پیام (mail) ارسالی',
                'verbose_name_plural': 'پیام (mail) های ارسالی',
            },
        ),
    ]