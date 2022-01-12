from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserNotification, AdminNotification
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


@receiver(post_save, sender=AdminNotification)
def notify_admin(sender, instance, created, **kwargs):
    if created:
        async_to_sync(channel_layer.group_send)(
            "notification_admin",
            {
                "type": "send_data",
                "data": {
                    "body": instance.body,
                    "self": False,
                    "fromUser": instance.fromUser.username,
                },
            },
        )


@receiver(post_save, sender=UserNotification)
def notify_admin(sender, instance, created, **kwargs):
    if created:
        async_to_sync(channel_layer.group_send)(
            f"notification_user_{instance.toUser.username}",
            {
                "type": "send_data",
                "data": {
                    "body": instance.body,
                    "self": False,
                },
            },
        )
