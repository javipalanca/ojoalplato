from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .models import Post


class RssLatestEntriesFeed(Feed):
    title = "Ojoalplato latests posts"
    link = "/feed/"
    description = "Últimas novedades y cambios en Ojoalplato."

    def items(self):
        return Post.objects.filter(status="publish").order_by('-post_date')[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content


class AtomLatestEntriesFeed(RssLatestEntriesFeed):
    feed_type = Atom1Feed
    subtitle = RssLatestEntriesFeed.description
