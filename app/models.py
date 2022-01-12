from django.db import models
from django.contrib.auth.models import User


class UserNotification(models.Model):
    toUser = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    body = models.TextField(null=False, blank=False)
    isRead = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.toUser} -> {self.body}"


class AdminNotification(models.Model):
    fromUser = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False
    )
    body = models.TextField(null=False, blank=False)
    isRead = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.fromUser} -> {self.body}"


class Message(models.Model):
    room_username = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False, related_name="room"
    )
    body = models.CharField(max_length=255, null=False, blank=False)
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False, related_name="sender"
    )

    def __str__(self):
        return f"{self.room_username} -> {self.body}"
