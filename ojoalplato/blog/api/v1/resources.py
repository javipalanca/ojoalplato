from drf_haystack.filters import HaystackAutocompleteFilter
from drf_haystack.viewsets import HaystackViewSet
from rest_framework.permissions import AllowAny

from ojoalplato.blog.api.v1.serializers import PostAutocompleteSerializer
from ojoalplato.blog.models import Post


class AutocompletePostSearchViewSet(HaystackViewSet):

    index_models = [Post]
    serializer_class = PostAutocompleteSerializer
    filter_backends = [HaystackAutocompleteFilter]
    permission_classes = [AllowAny]
