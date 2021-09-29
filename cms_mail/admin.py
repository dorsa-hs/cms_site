from django.contrib import admin
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import MailSetting, Mail
from django.conf import settings

# Register your models here.


admin.site.register(MailSetting)


@admin.action(description='Mark selected stories as published')
def send_prepared_mail(modeladmin, request, queryset):
    for mail in queryset:
        settings.EMAIL_HOST = mail.mail_service.email_host
        settings.EMAIL_HOST_USER = mail.mail_service.email_host_user
        settings.EMAIL_HOST_PASSWORD = mail.mail_service.email_host_password
        settings.EMAIL_USE_TLS = mail.mail_service.email_use_tls
        settings.EMAIL_PORT = mail.mail_service.email_port

        msg_html = render_to_string('email_template.html', {'mail': mail})

        receivers = []
        for receiver in list(mail.receiver.all()):
            receivers.append(receiver.email)

        is_sent = send_mail(
            mail.subject,
            mail.message,
            mail.mail_service.email_host,
            receivers,
            html_message=msg_html,

        )
        if is_sent:
            (queryset.update(status=0))  # status = sent
        else:
            (queryset.update(status=1))  # status = failed


@admin.register(Mail)
class MailModelAdmin(admin.ModelAdmin):
    list_display = ['subject', 'mail_service', 'created', 'last_updated', 'id', 'status']
    actions = ['send_prepared_mail']

    send_prepared_mail.short_description = "ارسال پیام (mail) های انتخاب شده"
    admin.site.add_action(send_prepared_mail)
