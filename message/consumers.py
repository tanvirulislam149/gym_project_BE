from channels.generic.websocket import AsyncWebsocketConsumer
import json

class MessageConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.private_room = f"chat_room_of_{self.room_name}"
        await self.channel_layer.group_add(self.private_room, self.channel_name)
        # await self.channel_layer.group_add("conversations", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.private_room, self.channel_name)
            # await self.channel_layer.group_discard("conversations", self.channel_name)

    async def send_message(self, event):
        await self.channel_layer.group_send(
            "conversations",
            {
                "type": "send_conversation_event",
                "id": event["conversation"]["id"],
                "has_unread": True
            }
        )
        await self.send(text_data=json.dumps(event))

    
    async def msg_read(self, event):
        await self.send(text_data=json.dumps(event))

    async def send_conversation(self, event):
        await self.send(text_data=json.dumps({
            "id": event["id"],
            "email": event["email"],
            "first_name": event["first_name"],
            "last_name": event["last_name"]
        }))


class ConversationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.private_room = f"conversations"
        await self.channel_layer.group_add(self.private_room, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.private_room, self.channel_name)
    
    async def receive(self, text_data):
        await self.send_conversation(json.loads(text_data))


    async def send_conversation(self, text_data):
        await self.channel_layer.group_send(
            "conversations",
            {
                "type": "send_conversation_event",
                "id": text_data["id"],
                "sender": {
                    "id": text_data["id"],
                    "email": text_data["sender"]["email"],
                    "image": text_data["sender"]["image"],
                    "first_name": text_data["sender"]["first_name"],
                    "last_name": text_data["sender"]["last_name"],
                },
                "has_unread": True
            }
        )

    async def send_conversation_event(self, event):
        await self.send(text_data=json.dumps(event))

