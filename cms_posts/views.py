from django.shortcuts import render

from cms_category.models import PostCategory
from .forms import NewCommentForm
from .models import Post, Comment
from django.views import generic
from django.http import HttpResponse, Http404


# class based views for posts
class PostList(generic.ListView):
    queryset = Post.objects.all().order_by('-created_on')
    template_name = 'post_list.html'
    paginate_by = 4


class PostsListByCategory(generic.ListView):
    template_name = 'post_list.html'
    paginate_by = 4

    def get_queryset(self):
        category_name = self.kwargs['category_name']
        category = PostCategory.objects.filter(name__iexact=category_name).first()
        if category is None:
            raise Http404('صفحه ی مورد نظر یافت نشد')
        return Post.objects.get_posts_by_category(category_name)

    def get_context_data(self, **kwargs):
        context = super(PostsListByCategory, self).get_context_data(**kwargs)
        category_name = self.kwargs['category_name']
        category = PostCategory.objects.get_queryset().filter(name=category_name)
        context['category_title'] = category.first()
        return context


# class PostDetail(generic.DetailView):
#     model = Post
#     template_name = 'post_view.html'


def post_detail(request, *args, **kwargs):
    comment_form = NewCommentForm(request.POST or None)
    selected_post_id = kwargs['post_id']
    post = Post.objects.get_by_id(selected_post_id)
    comments = Comment.objects.filter(blogpost_connected=post)
    if post is None:
        raise Http404('محصول مورد نظر یافت نشد')

    if comment_form.is_valid():
        content = request.POST.get('content')
        Comment.objects.create(blogpost_connected=post, author=request.user, content=content)
        comment_form = NewCommentForm()

    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form
    }

    return render(request, 'post_view.html', context)
