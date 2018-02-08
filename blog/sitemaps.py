from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9  # Maximum value is 1

    def items(self):
        return Post.published.all()

    # Receives each object returned by items() and returns the last time the
    # object was modified
    def lastmod(self, obj):
        return obj.publish