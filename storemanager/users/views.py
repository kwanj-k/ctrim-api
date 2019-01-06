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
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSerializer
from .models import UserProfile
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated



class Profile(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = UserProfile.objects.all()


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
