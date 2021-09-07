from django.contrib import admin
from django_jalali.admin.filters import JDateFieldListFilter
from .models import Post, Comment

# you need import this for adding jalali calander widget
import django_jalali.admin as jadmin


@admin.register(Post)
class BarAdmin(admin.ModelAdmin):
    list_filter = (
        ('created_on', JDateFieldListFilter),
    )


admin.site.register(Comment)
