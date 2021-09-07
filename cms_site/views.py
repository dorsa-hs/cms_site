from django.shortcuts import render
from cms_account.models import UserProfile
from cms_posts.models import Post, PostCategory
from cms_settings.models import SiteSetting


def home_page(request):
    home_categories = PostCategory.objects.filter(on_home=True)[:3]
    home_posts = {}

    for home_category in home_categories:
        home_posts[home_category] = Post.objects.filter(categories__title=home_category).order_by('-created_on')[:4]

    last_articles = Post.objects.order_by('-created_on')[:3]
    context = {
        'home_posts': home_posts.items(),
        'last_articles': last_articles
    }

    return render(request, "home_page.html", context)


def header(request, *args, **kwargs):
    site_setting = SiteSetting.objects.first()
    user_id = request.user.id
    user_profile_exist = UserProfile.objects.filter(user_id=user_id).exists()


    context = {
        'setting': site_setting,
        'user_profile_exist': user_profile_exist

    }
    return render(request, "shared/Header.html", context)


def footer(request, *args, **kwargs):
    site_setting = SiteSetting.objects.first()
    context = {
        'setting': site_setting
    }
    return render(request, "shared/Footer.html", context)


def home_banner(request, *args, **kwargs):
    context = {

    }
    return render(request, "shared/HomeBanner.html", context)


def banner(request, *args, **kwargs):
    print(kwargs)
    context = {

    }
    return render(request, "shared/Banner.html", context)


def posts_categories_partial(request):
    categories = PostCategory.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'shared/posts_categories_partial.html', context)
