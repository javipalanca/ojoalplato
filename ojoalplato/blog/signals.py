from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Post
from .tasks import send_newsletter


@receiver(pre_save, sender=Post)
def post_pre_save(sender, instance, **kwargs):
    print("Signal!!!", instance.id, instance.status)

    if instance.status == "publish":
        try:
            pre_instance = Post.objects.get(pk=instance.id)
            if pre_instance.status == "draft":
                print("Sending newsletter (draft->publish)")
                send_newsletter.apply_async((instance.id,), countdown=60*60)
        except Post.DoesNotExist:
            print("Sending newsletter (post.doesnotexist)")
            send_newsletter.apply_async((instance.id,), countdown=60*60)
