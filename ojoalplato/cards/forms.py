from haystack.forms import SearchForm


class RestaurantSearchForm(SearchForm):

    def no_query_found(self):
        return self.searchqueryset.all()
