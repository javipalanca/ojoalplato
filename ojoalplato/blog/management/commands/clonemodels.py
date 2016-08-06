# coding=utf-8
from django.core.management import BaseCommand
from wordpress.models import User, UserMeta, Post, PostMeta, Term, Taxonomy, Comment, TermTaxonomyRelationship

from ojoalplato.blog.models import Post as BlogPost, PostMeta as BlogPostMeta, Term as BlogTerm, \
    Taxonomy as BlogTaxonomy, Comment as BlogComment, TermTaxonomyRelationship as BlogTermTaxonomyRelationship, \
    ObjectDoesNotExist
from ojoalplato.users.models import User as BlogUser, UserMeta as BlogUserMeta


class Command(BaseCommand):
    help = 'Clone models from mysql to other db'

    def handle(self, *args, **options):

        for u in User.objects.using("mysql").all():
            user = BlogUser()
            user.login = u.login
            user.password = u.password
            user.username = u.username
            user.email = u.email
            user.url = u.url
            user.date_joined = u.date_registered
            user.activation_key = u.activation_key
            user.status = u.status
            user.name = u.display_name
            user.save(using="default")

        for m in UserMeta.objects.using("mysql").all():
            meta = BlogUserMeta()
            meta.id = m.id
            meta.key = m.key
            meta.value = m.value
            try:
                username = m.user.username
                user = BlogUser.objects.using("default").get(username=username)
                meta.user = user
            except ObjectDoesNotExist:
                pass
            meta.save(using="default")

        for t in Term.objects.using("mysql").all():
            term = BlogTerm()
            term.id = t.id
            term.name = t.name
            term.slug = t.slug
            term.group = t.group
            term.save(using="default")

        for t in Taxonomy.objects.using("mysql").all():
            taxonomy = BlogTaxonomy()
            taxonomy.id = t.id
            taxonomy.name = t.name
            taxonomy.description = t.description
            taxonomy.parent_id = t.parent_id
            taxonomy.count = t.count
            id = t.id
            try:
                term = BlogTerm.objects.using("default").get(id=id)
                taxonomy.term = term
            except ObjectDoesNotExist:
                pass
            taxonomy.save(using="default")

        for p in Post.objects.using("mysql").all():
            post = BlogPost()
            post.id = p.id
            post.guid = p.guid
            post.post_type = p.post_type
            post.status = p.status
            post.title = p.title
            post.slug = p.slug
            try:
                username = p.author.username
                author = BlogUser.objects.using("default").get(username=username)
                post.author = author
            except ObjectDoesNotExist:
                pass
            post.excerpt = p.excerpt
            post.content = p.content
            post.content_filtered = p.content_filtered
            post.post_date = p.post_date
            post.modified = p.modified

            # comment stuff
            post.comment_status = p.comment_status
            post.comment_count = p.comment_count

            # ping stuff
            post.ping_status = post.ping_status
            post.to_ping = p.to_ping
            post.pinged = p.pinged

            # statuses
            post.password = p.password

            # other various lame fields
            post.parent_id = p.parent_id
            post.menu_order = p.menu_order
            post.mime_type = p.mime_type

            post.save(using="default")

            for tt in p.terms.all():
                taxonomy = BlogTaxonomy.objects.get(id=tt.id)
                m1 = BlogTermTaxonomyRelationship(object=post, term_taxonomy=taxonomy, order=0)
                m1.save(using="default")

        for m in PostMeta.objects.using("mysql").all():
            meta = BlogPostMeta()
            meta.id = m.id
            meta.key = m.key
            meta.value = m.value
            try:
                id = m.post.id
                post = BlogPost.objects.using("default").get(id=id)
                meta.post = post
            except ObjectDoesNotExist:
                pass
            meta.save(using="default")

        for c in Comment.objects.using("mysql").all():
            comment = BlogComment()
            comment.id = c.id
            try:
                user = BlogUser.objects.using("default").get(id=c.user_id)
                comment.user = user
            except ObjectDoesNotExist:
                pass
            comment.parent_id = c.parent_id

            # author fields
            comment.author_name = c.author_name
            comment.author_email = c.author_email
            comment.author_url = c.author_url
            comment.author_ip = c.author_ip

            # comment data
            comment.post_date = c.post_date
            comment.content = c.content
            comment.karma = c.karma
            comment.approved = c.approved

            # other stuff
            comment.agent = c.agent
            comment.comment_type = c.comment_type
            try:
                id = c.id
                post = BlogPost.objects.using("default").get(id=id)
                comment.post = post
            except ObjectDoesNotExist:
                pass

            comment.save(using="default")
