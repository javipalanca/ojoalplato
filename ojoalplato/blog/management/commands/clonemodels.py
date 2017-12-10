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


def get_terms(p):
    terms_dict = collections.defaultdict(list)
    qs = Taxonomy.objects.using("mysql").filter(relationships__object_id=p.id).select_related()
    qs = qs.order_by('relationships__order', 'term__name')
    term_ids = [tax.term_id for tax in qs]
    terms = {}
    for term in Term.objects.using("mysql").filter(id__in=term_ids):
        terms[term.id] = term
    for tax in qs:
        if tax.term_id in terms:
            terms_dict[tax.name].append(terms[tax.term_id])

    return terms_dict


class Command(BaseCommand):
    help = 'Clone models from mysql to other db'

    def handle(self, *args, **options):

        print("Importing users")
        for u in tqdm(User.objects.using("mysql").all()):
            try:
                user = BlogUser.objects.using("default").get(username=u.username)
            except ObjectDoesNotExist:
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

        print("Importing users meta")
        for m in tqdm(UserMeta.objects.using("mysql").all()):
            try:
                meta = BlogUserMeta.objects.using("default").get(id=m.id)
            except ObjectDoesNotExist:
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

        print("Importing terms")
        for t in tqdm(Term.objects.using("mysql").all()):
            try:
                term = BlogTerm.objects.using("default").get(id=t.id)
            except ObjectDoesNotExist:
                term = BlogTerm()
            term.id = t.id
            term.name = t.name
            term.slug = t.slug
            term.group = t.group
            term.save(using="default")

        print("Importing taxonomies")
        for t in tqdm(Taxonomy.objects.using("mysql").all()):
            try:
                taxonomy = BlogTaxonomy.objects.using("default").get(id=t.id)
            except ObjectDoesNotExist:
                taxonomy = BlogTaxonomy()
            taxonomy.id = t.id
            taxonomy.name = t.name
            taxonomy.description = t.description
            taxonomy.parent_id = t.parent_id
            taxonomy.count = t.count
            comment_id = t.id
            try:
                term = BlogTerm.objects.using("default").get(id=comment_id)
                taxonomy.term = term
            except ObjectDoesNotExist:
                pass
            taxonomy.save(using="default")

        print("Importing posts")
        for p in tqdm(Post.objects.using("mysql").filter(status="publish")):
            try:
                post = BlogPost.objects.using("default").get(id=p.id)
            except ObjectDoesNotExist:
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
                try:
                    m1 = BlogTermTaxonomyRelationship.objects.get(object=post, term_taxonomy=taxonomy, order=0)
                except ObjectDoesNotExist:
                    m1 = BlogTermTaxonomyRelationship(object=post, term_taxonomy=taxonomy, order=0)
                m1.save(using="default")

        print("Importing posts meta")
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

        print("Importing comments")
        for c in tqdm(Comment.objects.using("mysql").all()):
            try:
                comment = BlogComment.objects.using("default").get(id=c.id)
            except ObjectDoesNotExist:
                comment = BlogComment()
            comment.id = c.id
            try:
                user = BlogUser.objects.using("default").get(id=c.user_id)
                comment.user = user
            except ObjectDoesNotExist:
                user = BlogUser()
                user.id = c.user_id
                user.username = c.user_id
                user.save(using="default")
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
                comment_id = c.id
                post = BlogPost.objects.using("default").get(id=comment_id)
                comment.post = post
            except ObjectDoesNotExist:
                pass

            comment.save(using="default")

        print("Importing categories and tags")
        # migrate Categories and Tags
        for p in tqdm(Post.objects.using("mysql").filter(status="publish")):
            try:
                post = BlogPost.objects.using("default").get(id=p.id)
                # print(p.title)
            except ObjectDoesNotExist:
                continue

            terms = get_terms(p)

            # print("Category: ", [x.name for x in terms["category"]])
            # print("Tags: ", [x.name for x in terms["post_tag"]])

            trans = {
                "Ir de vinos": "Vinos",
                "vinos": "Vinos"
            }

            if len(terms["category"]) > 0:
                category_str = terms["category"][0].name
                if category_str in trans.keys():
                    category_str = trans[category_str]
                try:
                    category = Category.objects.using("default").get(name=category_str)
                except ObjectDoesNotExist:
                    category = Category(name=category_str)
                    category.save(using="default")

                post.category = category

            for tag in terms["post_tag"]:
                post.tags.add(tag.name)

            post.save(using="default")

