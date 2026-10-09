from rest_framework import serializers
from plans.models import Plans, Fitness_classes_category, Scheduled_classes, Review
from django.utils.timezone import now
from user.models import CustomUser

class SimpleFitnessClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fitness_classes_category
        fields = ["id", "name"]

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name", "image"]

class PlansSerializer(serializers.ModelSerializer):
    fitness_classes = SimpleFitnessClassSerializer(many=True)
    class Meta:
        model = Plans
        fields = ["id", "type","months", "price", "fitness_classes"]

class CreatePlansSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = ["id", "type", "months", "price", "fitness_classes"]


class FitnessClassSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    class Meta:
        model = Fitness_classes_category
        fields = ["id", "name", "image", "description"]


class ScheduledClassSerializer(serializers.ModelSerializer):
    fitness_class = FitnessClassSerializer()
    class Meta:
        model = Scheduled_classes
        fields = ["id", "fitness_class", "date_time", "instructor", "total_seats", "booked_seats", "present_students"]


class CreateScheduledClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scheduled_classes
        fields = ["fitness_class", "date_time", "instructor", "total_seats"]

    def validate_date_time(self, dateTime):
        if dateTime <= now():
            raise serializers.ValidationError("Date and time must be in the future.")
        return dateTime
    

class ReviewSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only = True)

    class Meta:
        model = Review
        fields = ["id", "user", "rating", "comment", "fitness_class"]
        read_only_fields = ['fitness_class', "user"]

    def create(self, validated_data):
        id = self.context.get("fitness_class_id")
        return Review.objects.create(fitness_class_id = id, **validated_data) 