from rest_framework.renderers import BrowsableAPIRenderer,JSONRenderer
from rest_framework.generics import CreateAPIView
from .models import User
from .serializers import (
    SignupSerializer,
    LoginSerializer
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated,AllowAny
from common.permissions import IsOwnerOrReadOnly
from rest_framework.generics import GenericAPIView
from django.core.mail import send_mail
send_mail('Subject here', 'Here is the message.', 'from@example.com', ['to@example.com'], fail_silently=False)

# import sendgrid
# import os
# from sendgrid.helpers.mail import Email,Content,Mail


class SignupAPIView(CreateAPIView):
    permission_classes =(AllowAny,)
    renderer_classes = (BrowsableAPIRenderer,JSONRenderer,)
    serializer_class = SignupSerializer

    def post(self,request):
        user = request.data
        print(user)

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)



class Login(GenericAPIView):
    permission_classes = (AllowAny, )
    #renderer_classes = (UserJSONRenderer, )
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
