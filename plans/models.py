from django.db import models
from user.models import CustomUser
from cloudinary.models import CloudinaryField
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
class Plans(models.Model):
    MONTHLY = "Monthly" 
    THREE_MONTHS = "Three Months"
    HALF_YEARLY = "Half Yearly"
    YEARLY = "Yearly"
    TYPE_CHOICES = [
        (MONTHLY, "Monthly" ),
        (THREE_MONTHS, "Three Months" ),
        (HALF_YEARLY, "Half Yearly" ),
        (YEARLY, "Yearly" ),
    ]
    type = models.CharField(max_length=50, default="Monthly")
    months = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.type


class Fitness_classes_category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = CloudinaryField("image")
    plans = models.ManyToManyField(Plans, related_name="fitness_classes")
    
    def __str__(self):
        return f"{self.name}"
    

class Scheduled_classes(models.Model):
    fitness_class = models.ForeignKey(Fitness_classes_category, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    instructor = models.CharField(max_length=50)
    total_seats = models.PositiveIntegerField()
    booked_seats = models.PositiveIntegerField(default=0)
    present_students = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('fitness_class', 'date_time')

    def __str__(self):
        return f"{self.fitness_class.name} - {self.date_time}"
    

class Review(models.Model):
    fitness_class = models.ForeignKey(Fitness_classes_category, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"Review on {self.fitness_class.name} by {self.user.first_name}"