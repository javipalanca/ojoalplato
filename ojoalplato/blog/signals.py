import datetime
from django.utils import timezone

from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Post
from .tasks import post_published_task


@receiver(pre_save, sender=Post)
def blogpost_pre_save(sender, instance, **kwargs):
    print("Pre-Signal", instance.id, instance.status)

    if instance.status == "publish" and not instance.notified:
        now = timezone.now()
        delay = datetime.timedelta(hours=instance.notification_delay)
        post_date = instance.post_date
        eta = now+delay if post_date < now+delay else post_date
        try:
            pre_instance = Post.objects.get(pk=instance.id)
            if pre_instance.status == "draft":
                print("Sending newsletter (draft->publish)")
                post_published_task.apply_async((instance.id,), eta=eta)
        except Post.DoesNotExist:
            print("post.doesnotexist")
            post_published_task.apply_async((instance.id,), eta=eta)


@receiver(post_save, sender=Post)
def blogpost_post_save(sender, instance, created, **kwargs):
    print("Post-Signal", instance.id, instance.status)

    if created and instance.status == "publish" and not instance.notified:
        now = timezone.now()
        delay = datetime.timedelta(hours=instance.notification_delay)
        post_date = instance.post_date
        eta = now+delay if post_date < now+delay else post_date
        print("Sending newsletter (post.doesnotexist)")
        post_published_task.apply_async((instance.id,), eta=eta)
