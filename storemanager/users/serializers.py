from rest_framework import serializers
from django.contrib.auth import authenticate,get_user_model
import urllib.request
from .models import User
import re

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','email','password']

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Password should be atleast 8 characters long")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError(
                "Password should atleast have one integer")
        if value.isupper() or value.islower():
            raise serializers.ValidationError(
                "Password should contain both upper and lower case characters")
        if value.isdigit():
            raise serializers.ValidationError(
                "Password can not contain only integers")
        return value


    def create(self,validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255,read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self,data):
        username = data.get('email',None)
        password = data.get('password',None)
        user = authenticate(username=username, password=password)
        if not user:
            User = get_user_model()
            user_queryset = User.objects.all().filter(username__iexact=username)
            if not user_queryset:
                raise serializers.ValidationError(
                'User does not exist.'
                )
            username = user_queryset[0].email
            user = authenticate(username=username, password=password)
        return {
            'email':user.email,
            'username':user.username
        }
