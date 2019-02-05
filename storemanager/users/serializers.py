from rest_framework import serializers
from django.contrib.auth import authenticate,get_user_model
from .models import User
import re
from common.utils import get_jwt_token
from django.contrib.auth.hashers import make_password

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
    token = serializers.CharField(read_only=True)

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
        data['token'] = get_jwt_token(user)
        token = list(data.values())[2]
        return {
            'email':user.email,
            'username':user.username,
            'token':token
        }

class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def update(self, instance, validated_data):
        """Performs an update on a User."""

        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            
            setattr(instance, key, value)

        if password is not None:
            
            instance.set_password(password)

        instance.save()

        return instance
