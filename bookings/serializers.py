from rest_framework import serializers
from bookings.models import Book_plans, Book_Fitness_Classes, Payment_plans
from plans.models import Plans, Fitness_classes_category, Scheduled_classes
from decimal import Decimal 
from user.models import CustomUser
from django.utils.timezone import now
from dateutil.relativedelta import relativedelta

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "email"]

class SimplePlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plans
        fields = ["id", "type"]

class BookPlansSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    plans = SimplePlanSerializer()
    current_plan_days = serializers.SerializerMethodField(method_name="get_plan_dates")
    class Meta:
        model = Book_plans
        fields = ["id", "user", "plans", "price", "current_plan_days"]
        read_only_fields = ["user", "price", "current_plan_days"]

    def get_plan_dates(self, book_plans: Book_plans):
        plan = Payment_plans.objects.select_related("booked_plans").select_related("booked_plans__user").select_related("booked_plans__plans").filter(
            booked_plans_id = book_plans.id,
            start_date__lte=now(),
            end_date__gte=now()
        )
        if plan and plan[0]:
            return f"{plan[0].start_date} to {plan[0].end_date}"
        else:
            return "No active plan"

class CreateBookPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book_plans
        fields = ["id", "plans"]

    def create(self, validated_data):
        plan = validated_data["plans"]
        user = self.context["user"]
        if Book_plans.objects.filter(user = user).exists():
            raise serializers.ValidationError("You already have booked a plan. Try updating it...")
        
        return Book_plans.objects.create(user = user, price = Decimal(plan.price), **validated_data)

    def update(self, instance, validated_data):
        plan = validated_data["plans"]
        # if instance.price > plan.price:  
        #     raise serializers.ValidationError("You can't update from higher plans to lower plans.")
        
        instance.plans = plan
        instance.price = plan.price
        return super().update(instance, validated_data)


class SimpleFitnessClassSerializerForBooking(serializers.ModelSerializer):
    class Meta:
        model = Fitness_classes_category
        fields = ["id", "name", "description", "image"]


class SimpleScheduledClassSerializerForBooking(serializers.ModelSerializer):
    fitness_class = SimpleFitnessClassSerializerForBooking()
    class Meta:
        model = Scheduled_classes
        fields = ["id", "fitness_class", "date_time", "instructor"]


class BookClassSerializer(serializers.ModelSerializer):
    user = SimpleUserSerializer()
    scheduled_class = SimpleScheduledClassSerializerForBooking()
    class Meta:
        model = Book_Fitness_Classes
        fields = ["id", "user", "scheduled_class"]
        read_only_fields = ["user"]

class CreateBookClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book_Fitness_Classes
        fields = ["scheduled_class"]

    def validate_scheduled_class(self, scheduled_class):
        date_time = scheduled_class.date_time
        user = self.context["user"]
        plans = Payment_plans.objects.filter(
            booked_plans__user = user,
            start_date__lte=date_time,
            end_date__gte=date_time
        )
        if not plans.exists():
            raise serializers.ValidationError({"message": "This class is not in between your paid plans. Please buy or renew a plan."})
        if scheduled_class.date_time <= now():
            raise serializers.ValidationError("The date and time must be in the future.")
        return scheduled_class

    def create(self, validated_data):
        scheduled_class = validated_data["scheduled_class"]
        user = self.context["user"]
        if Book_Fitness_Classes.objects.filter(user = user, scheduled_class = scheduled_class).exists():
            raise serializers.ValidationError({"message": "You already have booked for this class."})

        if scheduled_class.total_seats == scheduled_class.booked_seats:
            raise serializers.ValidationError({"message": "No seat available in this class."})

        scheduled_class.booked_seats = scheduled_class.booked_seats + 1
        scheduled_class.save()
        return Book_Fitness_Classes.objects.create(user = user, **validated_data)
    
    def update(self, instance, validated_data):
        scheduled_class = validated_data["scheduled_class"]
        user = self.context["user"]
        if Book_Fitness_Classes.objects.filter(user = user, scheduled_class = scheduled_class).exists():
            raise serializers.ValidationError("You already have booked for this class.")
        
        return super().update(instance, validated_data)
    

class SimpleBookClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book_Fitness_Classes
        fields = ["id", "name", "date_time"]


class ClassAttendence(serializers.ModelSerializer):
    user = SimpleUserSerializer(read_only=True)
    scheduled_class= SimpleScheduledClassSerializerForBooking(read_only=True)
    class Meta:
        model = Book_Fitness_Classes
        fields = ["id", "user", "scheduled_class", "attendence"]

    def update(self, instance, validated_data):
        scheduled_class = instance.scheduled_class
        attendence = validated_data["attendence"]
        if attendence == "Present":
            scheduled_class.present_students += 1
        else:
            scheduled_class.present_students -= 1
            
        scheduled_class.save() 
        return super().update(instance, validated_data)


class PaymentPlansSerializer(serializers.ModelSerializer):
    booked_plans = BookPlansSerializer()
    class Meta:
        model = Payment_plans
        fields = ["id", "booked_plans", "amount", "start_date", "end_date", "status"]
        read_only_fields = ["amount"]


class CreatePaymentPlansSerializer(serializers.ModelSerializer):
    booked_plans = serializers.UUIDField()
    class Meta:
        model = Payment_plans
        fields = ["id", "booked_plans", "amount", "start_date", "status"]
        read_only_fields = ["amount"]

    def create(self, validated_data):
        planId = validated_data["booked_plans"]
        plan = Book_plans.objects.get(pk = planId)
        validated_data["end_date"] = validated_data["start_date"] + relativedelta(months=plan.plans.months)

        validated_data["booked_plans"] = plan 
        return Payment_plans.objects.create(amount = plan.price, **validated_data)
    