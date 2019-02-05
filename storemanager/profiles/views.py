from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

# Local application imports
from .models import UserProfile
from .serializers import ProfileSerialiazer
from rest_framework.renderers import BrowsableAPIRenderer,JSONRenderer


class ProfileListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerialiazer
    renderer_classes = (BrowsableAPIRenderer,JSONRenderer,)

    def get_queryset(self):
        queryset = UserProfile.objects.all().exclude(user=self.request.user)
        return queryset


class ProfileDetail(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerialiazer
    renderer_classes = (BrowsableAPIRenderer,JSONRenderer,)

    def get(self, request, username):
        try:
            profile = UserProfile.objects.get(user__username=username)
        except:
            msg = { "error": "Profile does not exist."}
            return Response(msg, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, username):
        profile = UserProfile.objects.get(user__username=username)
        if profile.user.username != request.user.username:
            msg = {"error": "You do not have permission to edit this profile."}
            return Response(msg, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        serializer = self.serializer_class(instance=request.user.profiles,
                                           data=data, partial=True)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
