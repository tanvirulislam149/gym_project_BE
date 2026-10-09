from django.db import models
from uuid import uuid4
from user.models import CustomUser

# Create your models here.


# Create your models here.
# class Message(models.Model):
#     id = models.UUIDField(primary_key=True, default = uuid4, editable=False)
#     sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="messages")
#     receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     message_text = models.TextField()
#     is_read = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.sender.id} X {self.receiver.id} X {self.message_text}"



##### New code starts from here -----------------
class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    sender = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="sender_convo")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.sender.email} X {self.id}"
    
class Message(models.Model):
    id = models.UUIDField(primary_key=True, default = uuid4, editable=False)
    message_sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="msg_sender")
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="message")
    message_text = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"