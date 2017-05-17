from celery import shared_task
from django.conf import settings
from django.contrib.sites.models import Site

from .models import Post
from newsletter.models import Article, Submission, Message, Newsletter

import requests
from facebook import GraphAPI


@shared_task
def post_published_task(post_id):
    send_newsletter(post_id=post_id)
    post_to_facebook(post_id=post_id)


def send_newsletter(post_id):
    print("send_newsletter activated")
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
    post.notified = True
    post.save()
    print("send_newsletter submitted")


def post_to_facebook(post_id):
    post = Post.objects.get(pk=post_id)
    if post.post_to_facebook:
        print("post_to_facebook activated")
        site = Site.objects.all()[0]
        page_access_token = get_fb_page_access_token()
        graph = GraphAPI(page_access_token)

        params = {"link": "http://{}{}".format(site.domain, post.get_absolute_url())}
        graph.post("{}/feed".format(settings.FACEBOOK_PAGE_ID), params=params)
        print("{} posted to facebook".format(post.id))


def get_fb_page_access_token():
    if settings.FACEBOOK_PAGE_ACCESS_TOKEN == "":
        params = {'client_id': settings.FACEBOOK_CLIENT_ID,
                  'client_secret': settings.FACEBOOK_CLIENT_SECRET,
                  'grant_type': 'client_credentials'}
        response = requests.get("https://graph.facebook.com/v2.8/oauth/access_token", params=params)
        user_access_token = response.json()["access_token"]
        user_graph = GraphAPI(user_access_token)
        accounts = user_graph.get("me/accounts")
        for page in accounts["data"]:
            if page["name"] == settings.FACEBOOK_PAGE_NAME:
                return page["access_token"]
    else:
        return settings.FACEBOOK_PAGE_ACCESS_TOKEN
