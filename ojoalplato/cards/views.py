from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from django.views.generic import DetailView, TemplateView
from django.http import HttpResponse

from ojoalplato.cards.forms import RestaurantSearchForm
from ojoalplato.cards.models import Restaurant

from haystack.forms import HighlightedModelSearchForm
from haystack.generic_views import SearchView
from haystack.query import SearchQuerySet

import json


# class MapView(SearchView):
#    model = Restaurant
#    template_name = "blog/wpfamily/map_list.html"
#    form = HighlightedModelSearchForm


class MapView(TemplateView):
    template_name = "blog/wpfamily/map_list.html"


class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = "cards/restaurant_detail.html"
    context_object_name = "card"


def restaurant_search(request):
    form = RestaurantSearchForm(request.GET)
    restaurants = form.search()
    paginator = Paginator(restaurants, 10)  # Show 10 results per page

    query = page = request.GET.get('q')
    page = request.GET.get('page')
    try:
        restaurants = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        restaurants = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        restaurants = paginator.page(paginator.num_pages)
    return render(request, 'blog/wpfamily/map_list.html',
                              {
                                  'query': query,
                                  'object_list': Restaurant.objects.all(),
                                  'page': restaurants
                              })


def autocomplete(request):
    sqs = SearchQuerySet().autocomplete(content_auto=request.GET.get('q', ''))[:5]
    suggestions = [result.title for result in sqs]
    # Make sure you return a JSON object, not a bare list.
    # Otherwise, you could be vulnerable to an XSS attack.
    the_data = json.dumps({
        'results': suggestions
    })
    return HttpResponse(the_data, content_type='application/json')
