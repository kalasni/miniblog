from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView

from .models import Post, PublishedManager
from .forms import EmailPostForm

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


def post_share(request, post_id):

    # Retrieve post by id
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        # Form was submitted
        form = EmailPostForm(request.POST)
        if form.is_valid():
            # Form fields passed validation
            # Return True if all data submitted are valid

            # This attribute is a dictionary of form fields and their values.
            cd = form.cleaned_data

            # send email
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'],
                 cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title,
                 post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'admin@miniblog.com', [cd['to']])
            sent = True

    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html',
         {'post': post, 'form': form, 'sent': sent})


