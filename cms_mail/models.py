import logging
from collections import namedtuple
from django.contrib import admin
from jsonfield import JSONField
from django.db import models
from django.core.exceptions import ValidationError
from django.template import Template, Context
from cms_contact.models import NewsletterSignUp
from django.core.mail import send_mail

# Create your models here.

logger = logging.getLogger(__name__)


class MailSetting(models.Model):
    name = models.CharField(verbose_name='نام', max_length=255)
    email_use_tls = models.BooleanField('EMAIL_USE_TLS', default=True)
    email_use_ssl = models.BooleanField('EMAIL_USE_SSL', default=False)
    email_ssl_keyfile = models.CharField('EMAIL_SSL_KEYFILE', max_length=1024, null=True, blank=True)
    email_ssl_certfile = models.CharField('EMAIL_SSL_CERTFILE', max_length=1024, null=True, blank=True)
    email_host = models.CharField('EMAIL_HOST', max_length=1024)
    email_host_user = models.CharField('EMAIL_HOST_USER', max_length=255)
    email_host_password = models.CharField('EMAIL_HOST_PASSWORD', max_length=255)
    email_port = models.PositiveSmallIntegerField('EMAIL_PORT', default=587)
    email_timeout = models.PositiveSmallIntegerField('EMAIL_TIMEOUT', null=True, blank=True)
    active = models.BooleanField(verbose_name='فعال', default=False)

    def save(self, *args, **kwargs):
        # Only one item can be active at a time

        if self.active:
            # select all other active items
            qs = type(self).objects.filter(active=True)
            # except self (if self already exists)
            if self.pk:
                qs = qs.exclude(pk=self.pk)
            # and deactive them
            qs.update(active=False)

        super(MailSetting, self).save(*args, **kwargs)

    def clean(self):
        if self.email_use_ssl and self.email_use_tls:
            raise ValidationError(
                "EMAIL_USE_TLS/EMAIL_USE_SSL are mutually exclusive, so only set one of those settings to True.")

    def __str__(self):
        return f"{self.name} - {self.email_host_user}"

    class Meta:
        verbose_name = 'تنظیم mail'
        verbose_name_plural = 'تنظیمات mail'


PRIORITY = namedtuple('PRIORITY', 'low medium high now')._make(range(4))
STATUS = namedtuple('STATUS', 'sent failed queued')._make(range(3))


class MailManager(models.Manager):
    def get_active_posts(self):
        return self.get_queryset().filter(active=True)

    def get_by_id(self, post_id):
        qs = self.get_queryset().filter(id=post_id)
        if qs.count() == 1:
            return qs.first()
        else:
            return None


class Mail(models.Model):
    STATUS_CHOICES = [(STATUS.sent, "sent"), (STATUS.failed, "failed"),
                      (STATUS.queued, "queued")]

    mail_service = models.ForeignKey(
        MailSetting,
        on_delete=models.CASCADE,
        verbose_name='سرویس mail',
        max_length=254,
    )

    receiver = models.ManyToManyField(
        NewsletterSignUp,
        verbose_name='ارسال به',
        max_length=254
    )
    # cc = CommaSeparatedEmailField(_("Cc"))
    # bcc = CommaSeparatedEmailField(_("Bcc"))

    # template = models.ForeignKey(
    #     EmailTemplate,
    #     verbose_name=_("Template"),
    #     null=True,
    #     blank=True,
    #     help_text=_("If template is selected, HTML message and "
    #                 "subject fields will not be used - they will be populated from template"),
    #     on_delete=models.CASCADE
    # )

    subject = models.CharField(
        verbose_name='موضوع پیام',
        max_length=989,
        blank=True
    )
    message = models.TextField(verbose_name='متن پیام', blank=True)

    # html_message = models.TextField(
    #     verbose_name=_("HTML Message"),
    #     blank=True,
    #     help_text=_("Used only if template is not selected")
    # )

    created = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated = models.DateTimeField(db_index=True, auto_now=True)

    status = models.PositiveSmallIntegerField(
        "Status",
        choices=STATUS_CHOICES, db_index=True,
        default=2, null=True)

    class Meta:
        verbose_name = 'پیام (mail) ارسالی'
        verbose_name_plural = 'پیام (mail) های ارسالی'

    def __init__(self, *args, **kwargs):
        super(Mail, self).__init__(*args, **kwargs)
        self._cached_email_message = None

    # @admin.action(description='Mark selected stories as published')
    # def make_sent(self, modeladmin, request, queryset):
    #     queryset.update(status='sent')

    def _get_context(self):
        context = {}
        # for var in self.templatevariable_set.all().filter(email=self):
        #     context[var.name] = var.value

        return Context(context)

    def email_message(self):
        if self._cached_email_message:
            return self._cached_email_message

        return self.prepare_email_message()

    def prepare_email_message(self):
        message = self.message
        return self._cached_email_message

    def save(self, *args, **kwargs):
        self.full_clean()
        super(Mail, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.subject) + " (" + str(self.mail_service.name) + ")"
