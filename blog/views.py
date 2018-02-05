from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from django.views.generic import ListView
from django.db.models import Count

from .models import Post, PublishedManager, Comment
from .forms import EmailPostForm, CommentForm

from taggit.models import Tag

def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 3) # 3 post in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)

    return render(request, 'blog/post/list.html', {'page': page,
                                                                           'posts': posts,
                                                                           'tag': tag})



# class PostListView(ListView):
#     """
#     Generic class-based view for a list of posts.
#     """
#     queryset = Post.published.all()

#     # It should be called post_list in the template, which is expected by ListView
#     context_object_name = 'posts'
#     #model = Post
#     paginate_by = 3
#     template_name = 'blog/post/list.html'

#     #def get_queryset(self):
#         #return Post.objects.filter(status='published')




def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                                                         status='published',
                                                         publish__year=year,
                                                         publish__month=month,
                                                         publish__day=day)

    # List of actives comments for this post.
    # We are building this QuerySet starting from the post object, using the
    # manager for related objects we defined as comments using the related_name
    # attribute of the relationship in the Comment model.
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        # A comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create a comment object but don't save to the db yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        # There is no POST request, so the view is called by a GET request
        comment_form = CommentForm()

    # List of similar posts
    # We are passing it flat=True to get a flat list like [1, 2, 3, ...]
    post_tags_id = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_id)\
                                                        .exclude(id=post.id)

    # We use the Count aggregation function to generate a calculated field
    # "same_tags" that contains the number of tags shared with all the
    # tags queried. Slice the result to retrieve only the first four posts.
    similar_posts = similar_posts.annotate(same_tags=Count('tags'))\
                                                        .order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog/post/detail.html', {'post': post,
                                                                               'comments': comments,
                                                                               'comment_form': comment_form,
                                                                               'similar_posts': similar_posts})


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


