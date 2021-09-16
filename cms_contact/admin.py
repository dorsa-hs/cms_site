from django.contrib import admin

# Register your models here.
from .models import ContactUs, NewsletterSignUp

admin.site.register(ContactUs)
admin.site.register(NewsletterSignUp)