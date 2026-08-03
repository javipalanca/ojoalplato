import operator
from functools import reduce

from drf_haystack.filters import HaystackAutocompleteFilter


class RankedHaystackAutocompleteFilter(HaystackAutocompleteFilter):
    """Prefer autocomplete matches in a result's title or name."""

    def process_filters(self, filters, queryset, view):
        if not filters:
            return filters

        priority_field = view.autocomplete_priority_field
        query_bits = []

        for fallback_field, query in filters.children:
            for word in query.split():
                cleaned_word = queryset.query.clean(word.strip())
                if not cleaned_word:
                    continue

                priority_match = view.query_object(
                    **{priority_field: cleaned_word},
                )
                fallback_match = view.query_object(
                    **{fallback_field: cleaned_word},
                )
                query_bits.append(priority_match | fallback_match)

        return reduce(operator.and_, query_bits) if query_bits else filters
