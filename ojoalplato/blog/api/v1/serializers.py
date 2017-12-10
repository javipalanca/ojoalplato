from drf_haystack.serializers import HaystackSerializer

from ojoalplato.blog.search_indexes import PostIndex


class PostAutocompleteSerializer(HaystackSerializer):

    class Meta:
        index_classes = [PostIndex]
        fields = ["title", "url", "img_src", "category", "content_auto"]
        ignore_fields = ["content_auto"]

        # The `field_aliases` attribute can be used in order to alias a
        # query parameter to a field attribute. In this case a query like
        # /search/?q=oslo would alias the `q` parameter to the `autocomplete`
        # field on the index.
        field_aliases = {
            "q": "content_auto"
        }
