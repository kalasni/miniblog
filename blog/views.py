from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView

from .models import Post, PublishedManager

# def post_list(request):
#     object_list = Post.published.all()
#     paginator = Paginator(object_list, 3) # 3 post in each page
#     page = request.GET.get('page')
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         # If page is not an integer deliver the first page
#         posts = paginator.page(1)
#     except EmptyPage:
#         # If page is out of range deliver last page of results
#         posts = paginator.page(paginator.num_pages)

#     return render(request, 'blog/post/list.html', {'posts': posts})


class PostListView(ListView):
    """
    Generic class-based view for a list of posts.
    """
    queryset = Post.published.all()

    # It should be called post_list in the template, which is expected by ListView
    context_object_name = 'posts'
    #model = Post
    paginate_by = 3
    template_name = 'blog/post/list.html'

    #def get_queryset(self):
        #return Post.objects.filter(status='published')


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                                         status='published',
                                                         publish__year=year,
                                                         publish__month=month,
                                                         publish__day=day)
    #return render(request,
                             #'blog/post/detail.html', {'page': page, 'post': post})

    return render(request, 'blog/post/detail.html', {'post': post})

