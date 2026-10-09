from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from user.models import CustomUser

class UserCreateSerializer(BaseUserCreateSerializer):
    image = serializers.ImageField(required=False, allow_null=True)
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ["id", "email","image", "first_name", "last_name", "password", "address", "phone_number"]


class UserSerializer(BaseUserSerializer):
    # is_staff = serializers.SerializerMethodField(method_name="get_is_staff")
    image = serializers.ImageField(required=False, allow_null=True)
    class Meta(BaseUserSerializer.Meta):
        fields = ["id", "email", "image","first_name", "last_name", "password", "address", "phone_number", "is_staff"]
    
    # def get_is_staff(self, user: CustomUser):
    #     return user.is_staff