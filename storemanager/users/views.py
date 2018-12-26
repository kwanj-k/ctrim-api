from rest_framework.renderers import BrowsableAPIRenderer,JSONRenderer
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import User
import urllib.request
from .serializers import (
    SignupSerializer,
    LoginSerializer
)
from django.contrib.auth import authenticate, login, get_user_model
from rest_framework_jwt.views import obtain_jwt_token
class SignupAPIView(CreateAPIView):
    permission_classes =(AllowAny,)
    renderer_classes = (BrowsableAPIRenderer,JSONRenderer,)
    serializer_class = SignupSerializer


class Login(CreateAPIView):
    permission_classes =(AllowAny,)
    serializer_class = LoginSerializer
    renderer_classes = (BrowsableAPIRenderer,JSONRenderer,)
    def post(self,request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
