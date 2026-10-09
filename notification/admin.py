from django.contrib import admin
from .models import Notification, NotificationMessage

# Register your models here.
admin.site.register(Notification)
admin.site.register(NotificationMessage)