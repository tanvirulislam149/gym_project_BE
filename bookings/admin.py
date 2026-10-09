from django.contrib import admin
from bookings.models import Book_plans, Book_Fitness_Classes, Payment_plans

# Register your models here.
admin.site.register(Book_plans)
admin.site.register(Book_Fitness_Classes)
admin.site.register(Payment_plans)