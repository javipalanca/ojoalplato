# coding=utf-8
import datetime

import collections
from autoslug import AutoSlugField
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import ForeignKey
from django.db.models import ImageField
from django.db.models import Q
from django.conf import settings
from model_utils.fields import MonitorField
from model_utils.models import TimeStampedModel
from django.utils import timezone

from taggit_autosuggest.managers import TaggableManager
from hitcount.models import HitCountMixin

from ojoalplato.cards.models import Restaurant, Wine, Recipe
from ojoalplato.users.models import User
from ojoalplato.category.models import Category

STATUS_CHOICES = (
    ('closed', 'closed'),
    ('open', 'open'),
)

POST_STATUS_CHOICES = (
    ('draft', 'borrador'),
    # ('inherit', 'inherit'),
    # ('private', 'private'),
    ('publish', 'publicado'),
)

POST_TYPE_CHOICES = (
    ('attachment', 'attachment'),
    ('page', 'page'),
    ('post', 'post'),
    ('revision', 'revision'),
)


class PostManager(models.Manager):
    """
    Provides convenience methods for filtering posts by status.
    """

    def _by_status(self, status, post_type='post'):
        now = timezone.now()
        return self.filter(status=status, post_type=post_type, post_date__lte=now) \
            .select_related().prefetch_related('meta')

    def drafts(self, post_type='post'):
        return self._by_status('draft', post_type)

    def private(self, post_type='post'):
        return self._by_status('private', post_type)

    def published(self, post_type='post'):
        return self._by_status('publish', post_type)

    def term(self, terms, taxonomy='post_tag'):
        """
        @arg terms Can either be a string (name of the term) or an list of term names.
        """

        terms = terms if isinstance(terms, (list, tuple)) else [terms]

        try:
            tx = Taxonomy.objects.filter(name=taxonomy, term__slug__in=terms)
            post_ids = TermTaxonomyRelationship.objects.filter(term_taxonomy__in=tx).values_list('object_id', flat=True)

            return self.published().filter(pk__in=post_ids)
        except Taxonomy.DoesNotExist:
            return self.none()

    def category(self, categories, taxonomy='category'):
        """
        @arg terms Can either be a string (name of the term) or an list of term names.
        """

        categories = categories if isinstance(categories, (list, tuple)) else [categories]

        try:
            tx = Taxonomy.objects.filter(name=taxonomy, term__slug__in=categories)
            post_ids = TermTaxonomyRelationship.objects.filter(term_taxonomy__in=tx).values_list('object_id', flat=True)

            return self.published().filter(pk__in=post_ids)
        except Taxonomy.DoesNotExist:
            return self.none()

    def from_path(self, path):

        (ymd, slug) = path.strip('/').rsplit('/', 1)

        start_date = datetime.datetime.strptime(ymd, "%Y/%m/%d")
        end_date = start_date + datetime.timedelta(days=1) - datetime.timedelta(minutes=1)

        params = {
            'post_date__range': (start_date, end_date),
            'slug': slug,
        }

        try:
            return self.published().get(**params)
        except ObjectDoesNotExist:
            pass  # fall through to return None


class TermTaxonomyRelationship(models.Model):
    object = models.ForeignKey('Post')
    term_taxonomy = models.ForeignKey('Taxonomy', related_name='relationships')
    order = models.IntegerField()

    class Meta:
        ordering = ['order']


def get_default_user():
    return User.objects.get(username="paco").pk


class Post(TimeStampedModel, HitCountMixin):
    """
    The mother lode.
    The WordPress post.
    """

    objects = PostManager()

    id = models.AutoField(primary_key=True)

    # post data
    guid = models.CharField(max_length=255, blank=True)
    post_type = models.CharField(max_length=20, choices=POST_TYPE_CHOICES, default="post")
    status = models.CharField(verbose_name="Estado", max_length=20, choices=POST_STATUS_CHOICES)
    title = models.CharField(verbose_name="Título", max_length=500)
    subtitle = models.CharField(verbose_name="Subtítulo", max_length=500, blank=True, null=True)
    slug = AutoSlugField(populate_from='title', verbose_name="Slug", max_length=200)
    author = models.ForeignKey(User, verbose_name="Autor", related_name='posts', blank=True, null=True,
                               default=get_default_user)
    excerpt = models.TextField(blank=True)
    content = models.TextField(verbose_name="Contenido")
    content_filtered = models.TextField(blank=True)
    post_date = models.DateTimeField(verbose_name="Fecha publicación", default=timezone.now)
    published_at = MonitorField(monitor='status', when=['publish'], verbose_name="Fecha publicación")
    modified_date = models.DateTimeField(blank=True, null=True)
    category = models.ForeignKey(Category, blank=True, null=True,
                                 verbose_name="Categoría")
    tags = TaggableManager(verbose_name="Etiquetas",
                           help_text="Lista de etiquetas separadas por comas.",
                           blank=True)

    image_header = ImageField(
        verbose_name="Imagen de cabecera",
        help_text="Imagen de 850px x 398px",
        upload_to=settings.MEDIA_ROOT,
        null=True, blank=True, )

    restaurant_card = ForeignKey(Restaurant, verbose_name="Ficha de restaurante",
                                 related_name="posts", blank=True, null=True,
                                 on_delete=models.SET_NULL)
    wine_card = ForeignKey(Wine, verbose_name="Ficha de vino", related_name="posts", blank=True, null=True)
    recipe_card = ForeignKey(Recipe, verbose_name="Ficha de receta", related_name="posts", blank=True, null=True)

    # comment stuff
    comment_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True, null=True)
    comment_count = models.IntegerField(default=0)

    # ping stuff
    ping_status = models.CharField(max_length=20, choices=STATUS_CHOICES, blank=True)
    to_ping = models.TextField(blank=True)
    pinged = models.TextField(blank=True)

    # statuses
    password = models.CharField(max_length=20, blank=True)
    #    category_id = models.IntegerField(db_column='post_category')

    # other various lame fields
    parent_id = models.IntegerField(default=0)
    # parent = models.ForeignKey('self', related_name="children", db_column="post_parent", blank=True, null=True)
    menu_order = models.IntegerField(default=0)
    mime_type = models.CharField(max_length=100, blank=True)

    terms = models.ManyToManyField('Taxonomy', through='TermTaxonomyRelationship', blank=True)

    term_cache = None
    child_cache = None

    notification_delay = models.PositiveSmallIntegerField(default=1, verbose_name="Retardo de notificación (horas)")
    notified = models.BooleanField(default=False, verbose_name="Notificación enviada")
    post_to_facebook = models.BooleanField(default=True, verbose_name="Publicar en Facebook")
    post_to_twitter = models.BooleanField(default=True, verbose_name="Publicar en Twitter")

    class Meta:
        get_latest_by = 'post_date'
        ordering = ["-post_date"]
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if self.parent_id is None:
            self.parent_id = 0
        super(Post, self).save(**kwargs)
        self.child_cache = None
        self.term_cache = None

    # cache stuff

    def _get_children(self):
        if self.child_cache is None:
            self.child_cache = list(Post.objects.filter(parent_id=self.pk))
        return self.child_cache

    def _get_terms(self, taxonomy):

        if not self.term_cache:

            self.term_cache = collections.defaultdict(list)

            qs = Taxonomy.objects.filter(relationships__object_id=self.id).select_related()
            qs = qs.order_by('relationships__order', 'term__name')

            term_ids = [tax.term_id for tax in qs]

            terms = {}
            for term in Term.objects.filter(id__in=term_ids):
                terms[term.id] = term

            for tax in qs:
                if tax.term_id in terms:
                    self.term_cache[tax.name].append(terms[tax.term_id])

        return self.term_cache.get(taxonomy)

    def _get_meta(self, key):
        meta = PostMeta.objects.get(Q(post=self) & Q(key=key))
        return meta.value

    # properties

    @property
    def children(self):
        return self._get_children()

    @property
    def parent(self):
        if self.parent_id:
            return Post.objects.get(pk=self.parent_id)

    @parent.setter
    def parent(self, post):
        if post.pk is None:
            raise ValueError('parent post must have an ID')
        self.parent_id = post.pk

    def views(self):
        metaviews, hits = int(self._get_meta("views")), int(self.hit_count.hits)
        return metaviews + hits

    # related objects

    def categories_terms(self):
        return self._get_terms("category")

    def attachments(self):
        for post in self._get_children():
            if post.post_type == 'attachment':
                yield {
                    'id': post.id,
                    'slug': post.slug,
                    'timestamp': post.post_date,
                    'description': post.content,
                    'title': post.title,
                    'guid': post.guid,
                    'mimetype': post.mime_type,
                }

    def tags_terms(self):
        return self._get_terms("post_tag")

    def get_absolute_url(self):
        return reverse("post-detail", args=[self.slug])


class PostMeta(models.Model):
    """
    Post meta data.
    """

    id = models.IntegerField(primary_key=True)
    post = models.ForeignKey(Post, related_name='meta', blank=True, null=True)
    key = models.CharField(max_length=255)
    value = models.TextField(blank=True)

    def __str__(self):
        return "{}: {}".format(self.key, self.value)


class Comment(models.Model):
    """
    Comments to Posts.
    """

    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, related_name="comments", blank=True, null=True)
    user = models.ForeignKey(User, related_name="comments", blank=True, null=True, default=0)
    parent_id = models.IntegerField(default=0)

    # author fields
    author_name = models.CharField(max_length=255)
    author_email = models.EmailField(max_length=100)
    author_url = models.URLField(blank=True)
    author_ip = models.GenericIPAddressField(blank=True, null=True)

    # comment data
    post_date = models.DateTimeField()
    content = models.TextField()
    karma = models.IntegerField()
    approved = models.CharField(max_length=20)

    # other stuff
    agent = models.CharField(max_length=255)
    comment_type = models.CharField(max_length=20)

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        if self.post:
            return u"%s on %s" % (self.author_name, self.post.title)
        else:
            return self.author_name

    def parent(self):
        return self._get_object(Comment, self.parent_id)

    def is_approved(self):
        return self.approved == '1'

    def is_spam(self):
        return self.approved == 'spam'


class Term(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    group = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Taxonomy(models.Model):
    id = models.IntegerField(primary_key=True)
    term = models.ForeignKey(Term, related_name='taxonomies', blank=True, null=True)
    name = models.CharField(max_length=32)
    description = models.TextField()
    parent_id = models.IntegerField(default=0)
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ['name']

    def __str__(self):
        try:
            term = self.term
        except Term.DoesNotExist:
            term = ''
        return "{0}: {1}".format(self.name, term)

    def parent(self):
        return self._get_object(Taxonomy, self.parent_id)
