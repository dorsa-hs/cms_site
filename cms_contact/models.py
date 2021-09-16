from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


# Create your models here.

class ContactUs(models.Model):
    full_name = models.CharField(max_length=150, verbose_name='نام و نام خانوادگی')
    email = models.EmailField(max_length=100, verbose_name='ایمیل')
    subject = models.CharField(max_length=200, verbose_name='عنوان پیام')
    text = RichTextUploadingField(null=True, blank=True, verbose_name='متن پیام', config_name='contact_form')
    is_read = models.BooleanField(verbose_name='خوانده شده / نشده')

    class Meta:
        verbose_name = 'پیام کاربر'
        verbose_name_plural = 'پیام های کاربران'

    def __str__(self):
        return self.subject


class NewsletterSignUp(models.Model):
    full_name = models.CharField(max_length=150, verbose_name='نام و نام خانوادگی')
    email = models.EmailField(max_length=100, verbose_name='ایمیل')

    class Meta:
        verbose_name = 'عضو خبرنامه'
        verbose_name_plural = 'اعضاء خبرنامه'

    def __str__(self):
        return self.email
