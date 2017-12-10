# coding=utf-8
import collections
from tqdm import tqdm
from django.core.management import BaseCommand
from wordpress.models import User, UserMeta, Post, PostMeta, Term, Taxonomy, Comment, TermTaxonomyRelationship

from ojoalplato.blog.models import Post as BlogPost, PostMeta as BlogPostMeta, Term as BlogTerm, \
    Taxonomy as BlogTaxonomy, Comment as BlogComment, TermTaxonomyRelationship as BlogTermTaxonomyRelationship, \
    ObjectDoesNotExist
from ojoalplato.category.models import Category
from ojoalplato.users.models import User as BlogUser, UserMeta as BlogUserMeta


class Command(BaseCommand):
    help = 'Clone models from mysql to other db'

    def handle(self, *args, **options):

       for m in tqdm(PostMeta.objects.using("mysql").all()):
            try:
                meta = BlogPostMeta.objects.using("default").get(id=m.id)
            except ObjectDoesNotExist:
                meta = BlogPostMeta()
            meta.id = m.id
            meta.key = m.key
            meta.value = m.value
            try:
                comment_id = m.post.id
                post = BlogPost.objects.using("default").get(id=comment_id)
                meta.post = post
            except ObjectDoesNotExist:
                pass
            meta.save(using="default")


