from django.contrib.auth import authenticate
from rest_framework_jwt.settings import api_settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User

def get_jwt_token(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    return jwt_encode_handler(payload)


class RegistrationSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super(RegistrationSerializer, self).__init__(*args, **kwargs)

        """
        Add custom error messages
        """
        for field in self.fields:
            error_messages = self.fields[field].error_messages
            error_messages['null'] = error_messages['blank'] \
                = error_messages['required'] \
                = 'Please supply your {}.'.format(field)

    username = serializers.RegexField(
        regex='^[A-Za-z\-\_]+\d*$',
        min_length=3,
        max_length=20,
        required=True,
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='The username already exists. Kindly try another.'
        )],
        error_messages={
            'min_length': 'Username allows a minimum of 3 characters.',
            'max_length': 'Username allows a maximum of 20 characters.',
            'invalid': 'Username should contain alphanumeric characters.'
        }
    )

    email = serializers.EmailField(
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Email already exists. '
                    'Please enter another email or sign in.'
        )],
        error_messages={
            'invalid': 'Please enter a valid email address.'
        }
    )

    password = serializers.RegexField(
        regex=r'^(?=.*[a-zA-Z])(?=.*[0-9])(?=.*[\!\@#\$%\^&]).*',
        max_length=128,
        min_length=8,
        write_only=True,
        error_messages={
            'max_length': 'Password allows a maximum of 128 characters.',
            'min_length': 'Password allows a minimum of 8 characters.',
            'invalid': 'Password must contain at least 1 letter, '
                       'a number and a special character.',
        })
    
    
    token = serializers.SerializerMethodField()

    def get_token(self, obj):
        token = get_jwt_token(obj)
        return token

    class Meta:
        model = User
        fields = ['email', 'username', 'token', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(username=email, password=password)
        if not user:
            user_queryset = User.objects.all().filter(username__iexact=email)
            if not user_queryset:
                raise serializers.ValidationError(
                    'Wrong email or password.'
                )
            username = user_queryset[0].email
            user = authenticate(username=username, password=password)
        data['token'] = get_jwt_token(user)
        return data


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'username',)
