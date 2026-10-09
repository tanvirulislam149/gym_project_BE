from django.contrib import admin
from plans.models import Plans, Fitness_classes_category, Scheduled_classes, Review

# Register your models here.
admin.site.register(Plans)
admin.site.register(Fitness_classes_category)
admin.site.register(Scheduled_classes)
admin.site.register(Review)