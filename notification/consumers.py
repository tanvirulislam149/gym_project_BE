from channels.generic.websocket import AsyncWebsocketConsumer
import json

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.private_room = f"notify_user_{self.room_name}"
        await self.channel_layer.group_add("public_notification", self.channel_name)
        await self.channel_layer.group_add(self.private_room, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard("public_notification", self.channel_name)
            await self.channel_layer.group_discard(self.private_room, self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'message': {
                'message_text': event["message"]
            },
            "is_read": event["is_read"]
        }))