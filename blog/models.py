from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# django-taggit
from taggit.managers import TaggableManager


# Custom model manager
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset() \
            .filter(status='published')


class Post(models.Model):

    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish')

    # We specify the name of the reverse relationship, from User to Post,
    # with the related_name attribute
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)

    # auto_now_add  - The date will saved when creating an object
    created = models.DateTimeField(auto_now_add=True)

    # auto_now - the date will be updated automatically when creating an object
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES,
                              default='draft')

    objects = models.Manager()  # The default manager

    # Custom manager. i.e, we can retrieve all published post whose title
    # starts with 'who' using:
    # Post.published.filter(title__startswith='Who')
    published = PublishedManager()

    tags = TaggableManager()

    class Meta:
        # Sort results by the publish field in descending order by default
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    # It returns the canonical URL of the object
    def get_absolute_url(self):
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])


class Comment(models.Model):
    """
    Model representing a comment
    """

    # The related_name attribute allows us to name the attribute that we use
    # for the relation from the related object back to this one.
    # If the related_name is not defined, Django will use the undercase name
    # of the model followed by _set (that is, comment_set)
    post = models.ForeignKey(Post, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.post)
