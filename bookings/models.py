from django.db import models
from user.models import CustomUser
from plans.models import Plans, Scheduled_classes
from uuid import uuid4

# Create your models here.
class Book_plans(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="booked_plan")
    plans = models.ForeignKey(Plans, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} X {self.plans}"
    

class Payment_plans(models.Model):
    PAYMENT_STATUS = [
        ("Not Paid", "Not Paid"),
        ("Paid", "Paid")
    ]
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    booked_plans = models.ForeignKey(Book_plans, on_delete=models.CASCADE, related_name="payment_status")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default = "Not Paid")

    def __str__(self):
        return f"{self.booked_plans.user.email} - {self.amount}"



class Book_Fitness_Classes(models.Model):
    ATTENDENCE_STATUS = [
        ("Absent", "Absent"),
        ("Present", "Present")
    ]
    id = models.UUIDField(primary_key=True, default = uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="booked_classes")
    scheduled_class = models.ForeignKey(Scheduled_classes, on_delete=models.CASCADE, default=3)
    attendence = models.CharField(max_length=30, choices=ATTENDENCE_STATUS, default="Absent")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} X {self.scheduled_class}"