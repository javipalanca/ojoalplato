# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import re_path
from django.views import defaults as default_views

from ojoalplato.blog.feed import RssLatestEntriesFeed, AtomLatestEntriesFeed
from ojoalplato.blog.sitemap import PostSitemap, SITEMAPS
from ojoalplato.blog.views import PostList, PostDetail, PostDetailById, CategoryList, TagList, AuthorList, \
    CategoriesList, TagsList, CategoriesAndTagsView
from ojoalplato.contactform.views import ContactFormView
from .router import urlpatterns as api_urlpatterns

admin.site.site_header = settings.ADMIN_SITE_HEADER

urlpatterns = [
    url(r'^maintenance-mode/', include('maintenance_mode.urls')),
    # url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^$', PostList.as_view(), name='home'),
    url(r'^about/$', PostList.as_view(), name='about'),
        #TemplateView.as_view(template_name='pages/about.html'), name='about'),
    # url(r'^wordpress/', include('wordpress.urls')),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, admin.site.urls),
    url(r'^adminactions/', include('adminactions.urls')),

    # User management
    # url(r'^users/', include('ojoalplato.users.urls', namespace='users')),
    # url(r'^accounts/', include('allauth.urls')),

    # 3rd party apps
    url(r'^redactor/', include('redactor.urls')),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^contact/', ContactFormView.as_view(), name="contact"),
    url(r'^contact/envelope/', include('envelope.urls')),
    # Subscriptions
    url(r'^subscription/', include('newsletter.urls')),

    # Haystack search
    #  url(r'^search/', include('haystack.urls')),

    # django-rest-framework
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    # Feed
    url('^feed/', RssLatestEntriesFeed(), name="feed"),
    url('^atom/', AtomLatestEntriesFeed(), name="atom"),

    # sitemap and robots.txt
    re_path(r'^sitemap\.xml', sitemap, {'sitemaps': SITEMAPS}, name='django.contrib.sitemaps.views.sitemap'),
    re_path(r'^robots\.txt', include('robots.urls')),

    # Blog app
    url(r'^(?P<slug>[-\w]+)/$', PostDetail.as_view(), name='post-detail'),
    url(r'^archivos/(?P<pk>\d+)/*$', PostDetailById.as_view(), name='post-detail-wp'),
    url(r'^archives/(?P<pk>\d+)/*$', PostDetailById.as_view(), name='post-detail-wp-en'),
    url(r'^author/(?P<author>[-\w]+)/$', AuthorList.as_view(), name='author-list'),


    url(r'^categories/and/tags/$', CategoriesAndTagsView.as_view(), name='more-list'),

    # Tags
    url(r'^tag/all/$', TagsList.as_view(), name='tags-list'),
    url(r'^tag/(?P<tag>[-\w]+)/$', TagList.as_view(), name='tag-list'),

    # Category app
    url(r'^category/all/$', CategoriesList.as_view(), name='categories-list'),
    url(r'^category/(?P<category>[-\w]+)/$', CategoryList.as_view(), name='category-list'),

    # Cards app
    url(r'^cards/', include(('ojoalplato.cards.urls', "cards"), namespace='cards')),

    # Guides app
    url(r'^guides/', include(('ojoalplato.guide.urls', "guide"), namespace='guides')),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# API URLs
# Create a router and register our resources with it.
urlpatterns += [
    url(r'^api/v1/', include((api_urlpatterns, "api_v1"), namespace="api_v1")),
]


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    import debug_toolbar
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
