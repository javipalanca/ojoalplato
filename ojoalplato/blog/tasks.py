from celery import shared_task
from django.contrib.sites.models import Site

from .models import Post
from newsletter.models import Article, Submission, Message, Newsletter


@shared_task
def send_newsletter(post_id):
    print("send_newsletter delayed!!!")
    post = Post.objects.get(pk=post_id)
    site = Site.objects.all()[0]

    newsletter = Newsletter.objects.all()[0]
    submission = Submission()
    message = Message()
    article = Article()
    article.url = "http://{}{}".format(site.domain, post.get_absolute_url())
    article.title = post.title
    article.text = post.content.replace('src="/media', 'src="http://'+site.domain+'/media')
    article.sortorder = 0

    message.title = post.title
    message.newsletter = newsletter
    message.slug = post.slug
    message.save()
    message.articles.add(article, bulk=False)
    message.save()
    article.save()

    submission.newsletter = newsletter
    submission.message = message
    submission.save()
    for s in newsletter.get_subscriptions():
        submission.subscriptions.add(s)
    submission.save()

    submission.submit()
    Submission.submit_queue()
    print("send_newsletter submitted!!!")
