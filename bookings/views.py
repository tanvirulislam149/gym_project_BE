from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from bookings.models import Book_plans, Book_Fitness_Classes, Payment_plans
from bookings.serializers import BookPlansSerializer, CreateBookPlanSerializer, BookClassSerializer, CreateBookClassSerializer, ClassAttendence, PaymentPlansSerializer, CreatePaymentPlansSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from sslcommerz_lib import SSLCOMMERZ
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseRedirect
from decouple import config
from django.db.models import Sum, Count
from notification.models import Notification, NotificationMessage
from user.models import CustomUser
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# Create your views here.
class BookPlansViewSet(ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_staff:
            return Book_plans.objects.all()
        return Book_plans.objects.filter(user = self.request.user)
    
    def get_permissions(self):
        if self.request.method in ["DELETE", "PUT", "PATCH"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def get_serializer_context(self):
        return {"user": self.request.user}
        
    def get_serializer_class(self):
        if self.request.method in ["POST", "PUT"]:
            return CreateBookPlanSerializer
        return BookPlansSerializer
    

class BookClassesViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.request.method in ["POST", 'PUT']:
            return CreateBookClassSerializer
        return BookClassSerializer
    
    def get_serializer_context(self):
        return {"user": self.request.user}
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Book_Fitness_Classes.objects.all()
        return Book_Fitness_Classes.objects.filter(user = self.request.user)
    
    def get_permissions(self):
        if self.request.method in ["DELETE"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]
        

class AttendenceViewSet(ModelViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("scheduled_class_id",)
    http_method_names = ["get", "put"]
    serializer_class = ClassAttendence

    def perform_update(self, serializer):
        serializer.save()
        data = serializer.data
        user = CustomUser.objects.get(id = data.get("user").get("id"))
        msg = f"Attendence marked as {data.get("attendence")} for {data.get("scheduled_class").get("fitness_class").get("name")} at {data.get("scheduled_class").get("date_time")} class"
        notification_msg = NotificationMessage.objects.create(message_text=msg)
        notification = Notification.objects.create(user=user, message=notification_msg)

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"notify_user_{user.id}",
            {
                "type": "send_notification",
                "message": msg,
                "is_read": False
            }
        )



    def get_queryset(self):
        if self.request.user.is_staff:
            return Book_Fitness_Classes.objects.all()
        return Book_Fitness_Classes.objects.filter(user = self.request.user)
    
    def get_permissions(self):
        if self.request.method == 'PUT':
            return [IsAdminUser()]
        return [IsAuthenticated()]
    

class PaymentPlansViewSet(ModelViewSet):
    def get_queryset(self):
        if self.request.user.is_staff:
            return Payment_plans.objects.select_related("booked_plans").select_related("booked_plans__user").select_related("booked_plans__plans").all().order_by("end_date")
        return Payment_plans.objects.filter(booked_plans__user = self.request.user).order_by("end_date")

    def get_serializer_class(self):
        if self.request.method in ['POST', "PUT"]:
            return CreatePaymentPlansSerializer
        return PaymentPlansSerializer
    
    def get_permissions(self):
        if self.request.method in ["PUT", "DELETE", "PATCH"]:
            return [IsAdminUser()]
        return [IsAuthenticated()]



@api_view(['POST'])
def initiate_payment(request):
    user = request.user
    amount = request.data.get("amount")
    payment_id = request.data.get("payment_id")

    settings = {'store_id': 'muscl681e1e55f1f11',
                'store_pass': 'muscl681e1e55f1f11@ssl', 'issandbox': True}
    sslcz = SSLCOMMERZ(settings)
    post_body = {}
    post_body['total_amount'] = amount
    post_body['currency'] = "BDT"
    post_body['tran_id'] = f"txn_{payment_id}"
    post_body['success_url'] = f"{config("BACKEND_URL")}/makePayment/success/"
    post_body['fail_url'] = f"{config("BACKEND_URL")}/makePayment/fail/"
    post_body['cancel_url'] = f"{config("BACKEND_URL")}/makePayment/cancel/"
    post_body['emi_option'] = 0
    post_body['cus_name'] = f"{user.first_name} {user.last_name}"
    post_body['cus_email'] = user.email
    post_body['cus_phone'] = user.phone_number
    post_body['cus_add1'] = user.address
    post_body['cus_city'] = "Dhaka"
    post_body['cus_country'] = "Bangladesh"
    post_body['shipping_method'] = "NO"
    post_body['multi_card_name'] = ""
    post_body['num_of_item'] = 1
    post_body['product_name'] = "Gym subscription"
    post_body['product_category'] = "General"
    post_body['product_profile'] = "general"

    response = sslcz.createSession(post_body)  # API response
    print(response)

    if response.get("status") == 'SUCCESS':
        return Response({"payment_url": response['GatewayPageURL']})
    return Response({"error": "Payment initiation failed"}, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def payment_success(request):
    payment_id = request.data.get("tran_id").split('_')[1]
    payment_plan = Payment_plans.objects.get(id=payment_id)
    payment_plan.status = "Paid"
    payment_plan.save()
    return HttpResponseRedirect(f"{config("FRONTEND_URL")}/dashboard/my_plans")


@api_view(['POST'])
def payment_cancel(request):
    payment_id = request.data.get("tran_id").split('_')[1]
    payment_plan = Payment_plans.objects.get(id=payment_id)
    payment_plan.delete()
    return HttpResponseRedirect(f"{config("FRONTEND_URL")}/dashboard/my_plans")


@api_view(['POST'])
def payment_fail(request):
    payment_id = request.data.get("tran_id").split('_')[1]
    payment_plan = Payment_plans.objects.get(id=payment_id)
    payment_plan.delete()
    return HttpResponseRedirect(f"{config("FRONTEND_URL")}/dashboard/my_plans")



class DashboardViewSet(ModelViewSet):
    http_method_names = ['get', "head", "options"]
    permission_classes = [IsAdminUser]
    
    def list(self, request):
        data = {
            "earning": Payment_plans.objects.aggregate(Sum("amount")),
            "Total_booked_class": Book_Fitness_Classes.objects.aggregate(Count("id")),
            "Total_payment": Payment_plans.objects.aggregate(Count("id")),
            "earning_data": Payment_plans.objects
            .values(
                'booked_plans__plans__type'
            )
            .annotate(total_amount=Sum('amount')),
            "booked_plan_data": Book_plans.objects
            .values(
                'plans__type'
            )
            .annotate(count=Count('id')),
            "booked_class_data": Book_Fitness_Classes.objects
            .values(
                'scheduled_class__fitness_class__name'
            )
            .annotate(count=Count('id')),
            "payment_records_data": Payment_plans.objects
            .values(
                'booked_plans__plans__type'
            )
            .annotate(count=Count('id'))
        }
        return Response(data)