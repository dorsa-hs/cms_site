from django.urls import path

from .views import contact_page, newsletter_signup

urlpatterns = [
    path('contact-us', contact_page),
    path('newsletter_signup', newsletter_signup, name='newsletter_signup'),
]
