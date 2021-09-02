from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_jalali.db import models as jmodels


class Comment(models.Model):
    blogpost_connected = models.ForeignKey(
        "cms_posts.Post", related_name='comments', on_delete=models.CASCADE, verbose_name='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='')
    content = models.TextField(verbose_name='')
    date_posted = jmodels.jDateField(default=timezone.now, verbose_name='تاریخ')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return str(self.author) + ' - ' + self.blogpost_connected.title[:40]

# def get_comments(self):
#     return self.objects.filter(blogpost_connected=self.get_object()).order_by('-date_posted')
