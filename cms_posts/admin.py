from django.contrib import admin
from .models import PostCategory
from django_jalali.admin.filters import JDateFieldListFilter

from .models import Post, Comment, PostCategory, Tag

# you need import this for adding jalali calander widget
import django_jalali.admin as jadmin


@admin.register(Post)
class BarAdmin(admin.ModelAdmin):
    list_filter = (
        ('created_on', JDateFieldListFilter),
    )


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name']

    class Meta:
        model = PostCategory


admin.site.register(Comment)
admin.site.register(Tag)
