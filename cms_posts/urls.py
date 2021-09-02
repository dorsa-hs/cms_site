from django.urls import path, include

from .views import post_detail, PostList, PostsListByCategory

urlpatterns = [
    path('news/', PostList.as_view(), name='posts'),
    path('news/<category_name>', PostsListByCategory.as_view(), name='posts_category'),
    path('news/<post_id>/<name>', post_detail, name='post_detail'),
]
