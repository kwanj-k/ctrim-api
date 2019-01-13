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
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ProfileSerializer,UserUpdateSerializer
from .models import UserProfile
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from common.permissions import IsOwnerOrReadOnly
from django.db.models import Q
from rest_framework.generics import GenericAPIView
from django.core.mail import send_mail
send_mail('Subject here', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=False)

# import sendgrid
# import os
# from sendgrid.helpers.mail import Email,Content,Mail




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

    def post(self,request):
        print(request.data['email'])
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()


        send_mail(
            'Email-verification',
            'Click here to verify your account ',
            'from@gmail.com',
            ['sender@gmail.com'],
            fail_silently=False,
        )
        info = """You have succesfully registerd to .., please check your email for a confirmation link"""
        rv = {"Message": info}
        return Response(rv, status=status.HTTP_201_CREATED)



class Login(GenericAPIView):
    permission_classes = (AllowAny, )
    #renderer_classes = (UserJSONRenderer, )
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
