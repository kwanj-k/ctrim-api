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
from .serializers import ProfileSerializer,UserUpdateSerializer
from .models import UserProfile
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from common.permissions import IsOwnerOrReadOnly
from django.db.models import Q



class Profile(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = UserProfile.objects.all()

class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    #permission_classes =(IsAuthenticated)
    serializer_class = ProfileSerializer
    lookup_field = 'slug'
    def get_queryset(self):
        slug = self.kwargs.get('slug')
        if slug:
            queryset = UserProfile.objects.filter(
					Q(slug__icontains=slug) |
					Q(slug__iexact=slug)
				)
        else:
            queryset = UserProfile.objects.all()
        if self.request.method == 'PUT':
            # queryset = UserProfile.everything.all()
            # return queryset
            self.serializer_class = UserUpdateSerializer
        return queryset


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
