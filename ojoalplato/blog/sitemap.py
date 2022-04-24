from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Post.objects.filter(status="publish")

    def lastmod(self, obj):
        return obj.post_date


SITEMAPS = {
    'post': PostSitemap,
}
