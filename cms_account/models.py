from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.user.username}{ext}"
    return f"profiles/{final_name}"


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, verbose_name='کاربر')
    avatar = models.ImageField(upload_to=upload_image_path, null=True, blank=True, verbose_name='آواتار')

    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل کاربران'

    def __str__(self):
        return self.user.username


def createProfile(sender, **kwargs):
    if kwargs['created']:
        user_profile = UserProfile.objects.created(user=kwargs['instance'])

    post_save.connect(createProfile, sender=User)
