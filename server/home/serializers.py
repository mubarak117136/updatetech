from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework.authtoken.models import Token

from .models import *

USER = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = USER
        fields = (
            "id",
            "username",
            "email",
        )

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class InvoiceSerializer(serializers.ModelSerializer):
    user_detail = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()

    def get_user_detail(self, obj):
        return UserSerializer(obj.user).data

    def get_items(self, obj):
        if obj.items.count() > 0:
            return ItemSerializer(data=obj.items.all(), many=True).data
        return None

    class Meta:
        model = Invoice
        fields = "__all__"


class MinimalInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = (
            "id",
            "name",
            "date",
            "due_date",
            "status"
        )


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(style={"placeholder": "Enter username!"})
    password1 = serializers.CharField(style={'input_type': 'password'})
    password2 = serializers.CharField(style={'input_type': 'password'})

    def validate_username(self, value):
        if value is None:
            raise ValidationError("Enter username!")
        if USER.objects.filter(username=value).exists():
            raise ValidationError("User exists!")
        return value    
    
    def validate(self, validated_data):
        password1 = validated_data.get("password1")
        password2 = validated_data.get("password2")               

        if len(password1) < 8:
            raise serializers.ValidationError({"password1": ["* Password is too short!", ]})
        else:
            if password1 != password2:
                raise serializers.ValidationError({"password1": ["* Password not matched!", ]})
        return validated_data
    
    def registered(self):
        username = self.validated_data.get("username")
        password1 = self.validated_data.get("password1")
                
        user = USER(username=username)
        user.set_password(password1)
        user.save()
        token, token_created = Token.objects.get_or_create(user=user)
        return user, token.key


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate_username(self, value):
        if value is None:
            raise serializers.ValidationError("Enter username!")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password need min 8 characters!")
        return value
    
    
    def validate(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password")
                
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({"username": ["* Username or Password not matched!", ]})
        else:
            if not user.is_active:
                raise serializers.ValidationError("* Account blocked! Please contact customer support!")
        return validated_data
    
    def sign_in(self):
        username = self.validated_data.get("username")
        password = self.validated_data.get("password")
        user = authenticate(username=username, password=password)
        return user