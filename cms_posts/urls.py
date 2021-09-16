from django.urls import path, include

from .views import post_detail, PostList, PostsListByCategory

urlpatterns = [
    path('news/', PostList.as_view(), name='posts'),
    path('news/<category_name>', PostsListByCategory.as_view(), name='posts_category'),
    path('news/<post_id>/<slug:slug>', post_detail, name='post_detail'),
    path('', include('cms_contact.urls')),
]
