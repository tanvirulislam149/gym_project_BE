from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from notification.models import Notification
from notification.serializers import NotificationSerializer
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response


# Create your views here.
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-message__created_at")

    def get_permissions(self):
        if self.action == "read_notification":
            return [IsAuthenticated()]
        if self.request.method == "POST":
            return [IsAdminUser()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=["post"])
    def read_notification(self, request):
        Notification.objects.filter(user = request.user, is_read=False).update(is_read=True)
        return Response({"update": "true"}, status=200)
