from django.apps import AppConfig


class CmsPostsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = "cms_posts"
    verbose_name = 'ماژول پست ها'


class CmsCommentsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cms_posts'
    verbose_name = 'ماژول نظرات'


class CmsCategoryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cms_posts'
    verbose_name = "دسته بندی ها"


class CmsTagsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cms_posts'
    verbose_name = 'ماژول برچسب ها'
