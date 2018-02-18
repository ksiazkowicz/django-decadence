# -*- coding: utf-8 -*-
from channels import Group
from channels.generic.websockets import JsonWebsocketConsumer


class UpdateConsumer(JsonWebsocketConsumer):
    """
    Update Consumer

    Handles logic for adding user sessions to specific Groups. Handles
    subscribe/unsubscribe requests.
    """
    http_user = True

    def connect(self, message, **kwargs):
        message.reply_channel.send({'accept': True})

    def receive(self, content, **kwargs):
        messages = content.get("batch", [content, ])

        for message in messages:
            subscribe = message.get("subscribe", False)
            group = message.get("group", None)

            if not group:
                continue

            if subscribe:
                Group(group).add(self.message.reply_channel)
            else:
                Group(group).remove(self.message.reply_channel)

    def disconnect(self, message, **kwargs):
        pass
