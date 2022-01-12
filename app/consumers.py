import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *


class UserNotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["username"]
        user = self.scope["user"]
        self.room_group_name = f"notification_user_{user.username}"

        if user.username == self.scope["url_route"]["kwargs"]["username"]:
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
            self.accept()
            self.user = user

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        """
        Format:
        {
            'body': 'hello 123',
            'self': False
        }
        * Self will be true, if the user send to the websocket,
          Self will be false, when django send through signals
        """
        data = json.loads(text_data)
        if data["self"] == False:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "send_data", "data": data}
            )
        else:
            AdminNotification.objects.create(fromUser=self.user, body=data["body"])

    def send_data(self, event):
        data = event["data"]
        self.send(text_data=json.dumps(data))


class AdminNotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "admin"
        user = self.scope["user"]
        self.room_group_name = "notification_admin"

        if user.is_superuser:
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
            self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        """
        Format:
        {
            'body': 'hello 123',
            'self': False,
            'fromUser': '<username>'
        }
        * Self will be true, if the admin send to the websocket,
          Self will be false, when django send through signals
        """
        data = json.loads(text_data)
        if data["self"] == False:
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "send_data", "data": data}
            )
        else:
            user = User.objects.get(username=data["fromUser"])
            UserNotification.objects.create(toUser=user, body=data["body"])

    def send_data(self, event):
        data = event["data"]
        self.send(text_data=json.dumps(data))


class ChatConsumer(WebsocketConsumer):
    def messagesSerializer(self, messages):
        result = []
        for message in messages:
            result.append(self.messageSerializer(message))
        return result

    def messageSerializer(self, message):
        result = {
            "body": message.body,
            "sender": message.sender.username,
        }
        return result

    def connect(self):
        username = self.scope["url_route"]["kwargs"]["username"]
        self.room_name = username
        self.username = username
        user = self.scope["user"]
        self.room_group_name = f"chat_{username}"

        if user.username == username or user.is_superuser:
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
            self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data):
        """
        Format:
        {
            'type': 'fetch_messages' / 'send_message',
            'body': 'hello 123',
            'sender': '<sender's username>',
        }
        """
        data = json.loads(text_data)
        room_user = User.objects.get(username=self.username)
        if data["type"] == "send_message":
            sender = User.objects.get(username=data["sender"])
            Message.objects.create(
                room_username=room_user, body=data["body"], sender=sender
            )
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name, {"type": "send_message", "message": data}
            )
        elif data["type"] == "fetch_messages":
            messages = Message.objects.filter(room_username=room_user)
            data = self.messagesSerializer(messages)
            self.send(text_data=json.dumps({"type": "fetch_messages", "data": data}))

    def send_message(self, event):
        data = event["message"]
        self.send(text_data=json.dumps(data))
