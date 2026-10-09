# from django.shortcuts import render
# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from message.models import Message
# from message.serializers import MessageSerializer, CreateMessageSerializer, ConversationSerializer
# from django.db.models import Q
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response 
# from user.models import CustomUser
# from user.serializers import UserSerializer
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from rest_framework.decorators import action



# # Create your views here.
# class MessageViewSet(ModelViewSet):
#     permission_classes = [IsAuthenticated]
    
#     def get_serializer_class(self):
#         if self.request.method == "POST":
#             return CreateMessageSerializer
#         return MessageSerializer

#     def get_queryset(self):   # get message url => /message/?receiver=1
#         receiver_id = self.request.query_params.get("receiver")
#         return Message.objects.select_related("sender").select_related("receiver").filter(Q(sender=self.request.user, receiver_id=receiver_id) | Q(sender=receiver_id, receiver_id=self.request.user)).order_by('created_at')


#     def perform_create(self, serializer):
#         # when the user send 1st message, conversation should show
#         sender = self.request.user.id 
#         validated_data = serializer.validated_data
#         receiver = validated_data.get("receiver")
#         # exists = Message.objects.filter(sender_id=sender).exists()

#         user = CustomUser.objects.filter(id=sender)
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#         f"conversation_{receiver.id}",
#             {
#                 "type": "send_conversation",
#                 "id": user[0].id,
#                 "email": user[0].email,
#                 "image": user[0].image.url if user[0].image else None,  # error coming from this line
#                 "first_name": user[0].first_name,
#                 "last_name": user[0].last_name
#             }
#         )
#         # After sending conversation, message is sent and saved

#         serializer.save()
#         data = serializer.data
#         room = [data.get("receiver"), data.get("sender")]
#         room.sort()
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             f"chat_room_of_{room[0]}and{room[1]}",
#             {
#                 "type": "send_message",
#                 "id": data.get("id"),
#                 "message_text": data.get("message_text"),
#                 "sender": data.get("sender"),
#                 "receiver": data.get("receiver"),
#                 "is_read": False
#             }
#         )

#     @action(detail=True, methods=["post"])
#     def read_message(self, request, pk = None):
#         # url => /message/message_id/read_message/
#         try:
#             msg = Message.objects.filter(id = pk).first()
#             if msg.receiver.id == self.request.user.id:
#                 msg.is_read = True
#                 msg.save()
#                 return Response({"message": "messsage is read."})
#             else:
#                 raise ValueError("Message not found")
#         except:
#             return Response({"error": "Something happend in the server."})





# @api_view(['GET'])
# @permission_classes([IsAdminUser])
# def get_conversations(request):
#     conversation_ids = Message.objects.values_list("sender", flat=True).distinct()
#     conversations = CustomUser.objects.filter(id__in = conversation_ids)
#     serializer = ConversationSerializer(conversations, many=True)
#     return Response(serializer.data)





######## New code starts from here ----------------
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from message.models import Conversation, Message
from message.serializers import ConvoSerializer, CreateConvoSerializer, MessageSerializer, CreateMessageSerializer
from rest_framework.exceptions import ValidationError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from rest_framework.decorators import action
from rest_framework.response import Response

class ConvoViewset(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Conversation.objects.all()
        else:
            return Conversation.objects.filter(sender = self.request.user)

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return CreateConvoSerializer
        return ConvoSerializer
    
    def perform_create(self, serializer):
        exists = Conversation.objects.filter(sender = self.request.user).first()
        if not exists:
            serializer.save(sender = self.request.user)
        else:
            raise ValidationError({"Error": "Conversation already exists"})


class MessageViewset(ModelViewSet):
    # queryset = Message.objects.all()
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        data = serializer.validated_data
        user_id = data["conversation"].sender.id
        serializer.save()
        saved_data = serializer.data 
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_room_of_{user_id}",
            {
                "type": "send_message",
                "id": saved_data.get("id"),
                "conversation": {
                    "id": str(data.get("conversation").id),
                    "sender": {
                        "id": data.get("conversation").sender.id,
                        "email": data.get("conversation").sender.email,
                    }
                },
                "message_sender": data.get("message_sender").id,
                "message_text": data.get("message_text"),
                "is_read": False
            }
        )

    @action(detail=True, methods=["post"])
    def read_message(self, request, pk = None):
        # url => /message/message_id/read_message/
        try:
            msg = Message.objects.filter(id = pk).first()
            if msg.message_sender.id != self.request.user.id:
                channel_layer = get_channel_layer()
                async_to_sync(channel_layer.group_send)(
                    f"chat_room_of_{msg.conversation.sender.id}",
                    {
                        "type": "msg_read",
                        "id": str(msg.id),
                        "is_read": True
                    }
                )
                msg.is_read = True
                msg.save()
                return Response({"message": "messsage is read."})
            else:
                raise ValueError("Message not found")
        except:
            return Response({"error": "Something happend in the server."})
        

    def get_queryset(self):   # get message url => /message/?convo_id=id
        convo_id = self.request.query_params.get("convo_id")
        return Message.objects.select_related("conversation").select_related("conversation__sender").filter(conversation_id = convo_id).order_by('created_at')

    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT", "PATCH"]:
            return CreateMessageSerializer
        return MessageSerializer 


