"""cms_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from cms_site import settings
from .views import home_page, header, footer, home_banner, banner, posts_categories_partial

urlpatterns = [
    path('', home_page),
    path('header', header, name='header'),
    path('footer', footer, name='footer'),
    path('home-banner', home_banner, name='home_banner'),
    path('posts_categories_partial', posts_categories_partial, name='posts_categories_partial'),
    path('banner', banner, name='banner'),
    path('', include('cms_account.urls')),
    path('', include('cms_contact.urls')),
    path('', include('cms_posts.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
