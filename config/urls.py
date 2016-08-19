# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views

from ojoalplato.blog.views import PostList, PostDetail, PostDetailById, CategoryList, TagList, AuthorList

urlpatterns = [
    # url(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    url(r'^$', PostList.as_view(), name='home'),
    # url(r'^about/$', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    # url(r'^wordpress/', include('wordpress.urls')),
    # Django Admin, use {% url 'admin:index' %}
    url(settings.ADMIN_URL, include(admin.site.urls)),

    # User management
    url(r'^users/', include('ojoalplato.users.urls', namespace='users')),
    # url(r'^accounts/', include('allauth.urls')),

    # Blog app
    url(r'^(?P<slug>[-\w]+)/$', PostDetail.as_view(), name='post-detail'),
    url(r'^archivos/(?P<pk>\d+)/*$', PostDetailById.as_view(), name='post-detail-wp'),
    url(r'^archives/(?P<pk>\d+)/*$', PostDetailById.as_view(), name='post-detail-wp-en'),
    url(r'^tag/(?P<tag>[-\w]+)/$', TagList.as_view(), name='tag-list'),
    url(r'^author/(?P<author>[-\w]+)/$', AuthorList.as_view(), name='author-list'),

    # Category app
    url(r'^category/(?P<category>[-\w]+)/$', CategoryList.as_view(), name='category-list'),

    # Your stuff: custom urls includes go here
    url(r'^redactor/', include('redactor.urls')),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        url(r'^400/$', default_views.bad_request, kwargs={'exception': Exception('Bad Request!')}),
        url(r'^403/$', default_views.permission_denied, kwargs={'exception': Exception('Permission Denied')}),
        url(r'^404/$', default_views.page_not_found, kwargs={'exception': Exception('Page not Found')}),
        url(r'^500/$', default_views.server_error),
    ]
