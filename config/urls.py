# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from ojoalplato.blog.feed import RssLatestEntriesFeed, AtomLatestEntriesFeed
from ojoalplato.blog.sitemap import PostSitemap, SITEMAPS
from ojoalplato.blog.views import PostList, PostDetail, PostDetailById, CategoryList, TagList, AuthorList, \
    CategoriesList, TagsList, CategoriesAndTagsView
from ojoalplato.contactform.views import ContactFormView

admin.site.site_header = settings.ADMIN_SITE_HEADER

urlpatterns = [
    path('maintenance-mode/', include('maintenance_mode.urls')),
    # path(r'^$', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('', PostList.as_view(), name='home'),
    path('about/', PostList.as_view(), name='about'),
    # TemplateView.as_view(template_name='pages/about.html'), name='about'),
    # path(r'^wordpress/', include('wordpress.urls')),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path('adminactions/', include('adminactions.urls')),

    # User management
    # path(r'^users/', include('ojoalplato.users.urls', namespace='users')),
    # path(r'^accounts/', include('allauth.urls')),

    # 3rd party apps
    path('redactor/', include('redactor.urls')),
    path('taggit_autosuggest/', include('taggit_autosuggest.urls')),
    path('contact/', ContactFormView.as_view(), name="contact"),
    path('contact/envelope/', include('envelope.urls')),
    # Subscriptions
    path('subscription/', include('newsletter.urls')),

    # Haystack search
    #  path(r'^search/', include('haystack.urls')),


    # Feed
    path('feed/', RssLatestEntriesFeed(), name="feed"),
    path('atom/', AtomLatestEntriesFeed(), name="atom"),

    # sitemap and robots.txt
    path('sitemap.xml', sitemap, {'sitemaps': SITEMAPS}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),

    # Blog app
    re_path(r'^(?P<slug>[-\w]+)/$', PostDetail.as_view(), name='post-detail'),
    path('archivos/<int:pk>/*', PostDetailById.as_view(), name='post-detail-wp'),
    path('archives/<int:pk>/*', PostDetailById.as_view(), name='post-detail-wp-en'),
    path('author/<str:author>/', AuthorList.as_view(), name='author-list'),

    path('categories/and/tags/', CategoriesAndTagsView.as_view(), name='more-list'),

    # Tags
    path('tag/all/', TagsList.as_view(), name='tags-list'),
    path('tag/<str:tag>/', TagList.as_view(), name='tag-list'),

    # Category app
    path('category/all/', CategoriesList.as_view(), name='categories-list'),
    path('category/<str:category>/', CategoryList.as_view(), name='category-list'),

    # Cards app
    path('cards/', include(('ojoalplato.cards.urls', "cards"), namespace='cards')),

    # Guides app
    path('guides/', include(('ojoalplato.guide.urls', "guide"), namespace='guides')),

    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [
    # API base url
    path("api/v1/", include("config.api_router")),
    # DRF auth token
    path("api/auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    # django-rest-framework
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
