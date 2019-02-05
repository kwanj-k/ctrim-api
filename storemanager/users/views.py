from rest_framework.renderers import BrowsableAPIRenderer,JSONRenderer
from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import (
    SignupSerializer,
    LoginSerializer,
    UserSerializer
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated,AllowAny
from common.permissions import IsOwnerOrReadOnly
from rest_framework.generics import GenericAPIView
from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth1, BaseOAuth2
from social_core.exceptions import MissingBackend
from common.utils import get_jwt_token


class SignupAPIView(CreateAPIView):
    permission_classes =(AllowAny,)
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,)
    serializer_class = SignupSerializer

    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class Login(GenericAPIView):
    permission_classes = (AllowAny, )
    renderer_classes = (BrowsableAPIRenderer, JSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SocialAuth(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (JSONRenderer,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        provider = request.data['provider']
        strategy = load_strategy(request)
        if 'access_token_secret' in request.data:
            token = {
                'oauth_token': request.data['access_token'],
                'oauth_token_secret': request.data['access_token_secret']
            }
        else:
            token = request.data.get('access_token')
        try:
            backend = load_backend(
                strategy=strategy,
                name=provider,
                redirect_uri=None
            )
        except MissingBackend:
            message = {"error": "Please enter a valid provider."}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = backend.do_auth(token)
        except BaseException:
            return Response({"error": "Invalid token."},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(user)
        serializer_data = serializer.data
        serializer_data["token"] = get_jwt_token(user)
        return Response(serializer_data, status=status.HTTP_200_OK)
