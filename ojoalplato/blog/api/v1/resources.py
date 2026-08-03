from drf_haystack.viewsets import HaystackViewSet
from rest_framework.permissions import AllowAny

from ojoalplato.blog.api.v1.serializers import PostAutocompleteSerializer
from ojoalplato.blog.models import Post
from ojoalplato.search_filters import RankedHaystackAutocompleteFilter


class AutocompletePostSearchViewSet(HaystackViewSet):

    index_models = [Post]
    serializer_class = PostAutocompleteSerializer
    filter_backends = [RankedHaystackAutocompleteFilter]
    autocomplete_priority_field = "title_auto"
    permission_classes = [AllowAny]
