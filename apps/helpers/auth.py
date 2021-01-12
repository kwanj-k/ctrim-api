"""Authenticate the user to allow client to hit the endpoints."""


from functools import wraps

import base64
import jwt

from decouple import config
from django.conf import settings
from rest_framework import status, authentication, exceptions
from rest_framework.response import Response

from apps.helpers.response_messages import auth_messages
from apps.users.models import User


EXEMPTED = ('/', '/api/docs/')



def get_token(request):
    """Get token from cookie or header."""
    token = request.COOKIES.get('jwt-token')
    if token is None:
        token = request.META.get('HTTP_AUTHORIZATION')
    return token


def decode_token(token):
    """Decode token with relevant key."""
    public_key = config('PUBLIC_KEY')
    try:
        return jwt.decode(token[7:], verify=False)
    except jwt.exceptions.ExpiredSignatureError:
        data = {
            'status': 'error',
            'error': 'token_expired',
            'message': 'Get a new token'
        }
        raise exceptions.AuthenticationFailed(
            data, status.HTTP_401_UNAUTHORIZED)
    except jwt.exceptions.InvalidTokenError:
        data = {
            'status': 'error',
            'error': 'Invalid token',
            'message': 'Ensure you are using a Goauth token'
        }
        raise exceptions.AuthenticationFailed(
            data, status.HTTP_400_BAD_REQUEST)


class GoauthJWTAuthentication(authentication.BaseAuthentication):
    """Authentication class for the application."""

    def authenticate(self, request):
        """Authenticate a user and return the user if authenticated."""
        if request.path in EXEMPTED:
            return None
        token = get_token(request)
        if not token:
            raise exceptions.AuthenticationFailed(auth_messages["token_required"],
                                                  status.HTTP_400_BAD_REQUEST)

        # set token to the session
        request.session['goauth-jwt-token'] = token
        try:
            payload = decode_token(token)
            try:
                user = User.objects.get(email=payload["email"])
                return (user, None)
            except User.DoesNotExist:
                return None
        except jwt.exceptions.ExpiredSignatureError:
            return Response(*auth_messages["expired_token"], status=status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.InvalidTokenError:
            return Response(*auth_messages["invalid_token"], status=status.HTTP_401_UNAUTHORIZED)
