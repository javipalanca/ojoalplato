from django.utils import timezone
from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    title = indexes.CharField(model_attr='title', null=True)
    title_auto = indexes.EdgeNgramField(model_attr='title', null=True, boost=2.0)
    url = indexes.CharField(model_attr="url", null=True)
    img_src = indexes.CharField(model_attr="img_src", null=True)
    category = indexes.CharField(model_attr="category", null=True)
    # We add this for autocomplete.
    content_auto = indexes.EdgeNgramField(model_attr='autocomplete_text')

    status = indexes.CharField(model_attr='status')
    post_date = indexes.DateTimeField(model_attr='post_date')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        # return self.get_model().objects.published()
        return self.get_model().objects.filter(status='publish', post_date__lte=timezone.now())
