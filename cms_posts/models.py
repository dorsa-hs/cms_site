import os

from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
from django.utils import timezone
from cms_category.models import PostCategory

STATUS = (
    (0, "Draft"),
    (1, "Publish"),
    (2, "Delete")
)


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    name, ext = get_filename_ext(filename)
    final_name = f"{instance.id}-{instance.title}{ext}"
    return f"posts/{final_name}"


class PostManager(models.Manager):
    def get_active_posts(self):
        return self.get_queryset().filter(active=True)

    def get_posts_by_category(self, category_name):
        return self.get_queryset().filter(categories__name__iexact=category_name, active=True)

    def get_by_id(self, post_id):
        qs = self.get_queryset().filter(id=post_id)
        if qs.count() == 1:
            return qs.first()
        else:
            return None


class Post(models.Model):
    title = models.CharField(max_length=200, unique=True, verbose_name='عنوان')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='عنوان در url')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    # and date time fields automatically populated using system time
    # updated_on = models.DateTimeField(auto_now=True)
    created_on = jmodels.jDateField(verbose_name='تاریخ')
    content = RichTextUploadingField(null=True, blank=True, verbose_name='محتوا')
    active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    categories = models.ManyToManyField(PostCategory, blank=True, verbose_name="دسته بندی ها")

    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True, verbose_name='تصویر')

    # meta description for SEO benifits
    # metades = models.CharField(max_length=300, default="new post")
    # status of post
    # status = models.IntegerField(choices=STATUS, default=0)

    objects = PostManager()

    # meta for the class
    class Meta:
        ordering = ['-created_on']
        # fields = ('name', 'date', 'date_time')
        verbose_name = 'پست'
        verbose_name_plural = 'پست ها'

    def __str__(self):
        return "%s, %s" % (self.title, self.created_on)

    def get_absolute_url(self):
        return f"/news/{self.id}/{self.slug}"

    @property
    def number_of_comments(self):
        return Comment.objects.filter(blogpost_connected=self).count()


class Comment(models.Model):
    blogpost_connected = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE, verbose_name='پست')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده نظر')
    content = models.TextField(verbose_name='محتوا')
    date_posted = jmodels.jDateField(default=timezone.now, verbose_name='تاریخ')

    class Meta:
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return str(self.author) + ' - ' + self.blogpost_connected.title[:40]
