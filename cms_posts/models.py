import os
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django_jalali.db import models as jmodels
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django_resized import ResizedImageField
from io import BytesIO
from django.core.files import File
from PIL import Image
from .utils import unique_slug_generator
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

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


def make_thumbnail(image, size=(170, 170)):
    """Makes thumbnails of given size from given image"""

    im = Image.open(image)

    im.convert('RGB')  # convert mode

    im.thumbnail(size)  # resize image

    thumb_io = BytesIO()  # create a BytesIO object

    im.save(thumb_io, 'JPEG', quality=80)  # save image to BytesIO object

    thumbnail = File(thumb_io, name=image.name)  # create a django friendly File object

    return thumbnail


class PostCategory(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان')
    name = models.CharField(max_length=150, verbose_name='عنوان در URL')
    on_home = models.BooleanField(default=False, verbose_name='نمایش دسته در خانه')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.title


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
    # image = models.ImageField(upload_to=upload_image_path, null=True, blank=True, verbose_name='تصویر')
    image = ResizedImageField(size=[730, 730], quality=90, upload_to=upload_image_path,
                              null=True, blank=True, verbose_name='تصویر')
    thumbnail = ImageSpecField(source='image',
                               processors=[ResizeToFill(170, 100)],
                               format='JPEG',
                               options={'quality': 70})
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


class Tag(models.Model):
    title = models.CharField(max_length=120, verbose_name='عنوان')
    slug = models.SlugField(verbose_name='عنوان در url')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    active = models.BooleanField(default=True, verbose_name='فعال / غیر فعال')
    posts = models.ManyToManyField(Post, blank=True, verbose_name='پست ها')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'برچسب / تگ'
        verbose_name_plural = 'برچسب ها / تگ ها'


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(tag_pre_save_receiver, sender=Tag)
