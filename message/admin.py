from django.contrib import admin
from message.models import Message, Conversation

# Register your models here.
admin.site.register(Conversation)
admin.site.register(Message)