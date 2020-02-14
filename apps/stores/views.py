from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Store
from .serializers import StoreSerializer


class StoreListCreateView(ListCreateAPIView):
    """ List/Create stores"""
    serializer_class = StoreSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Store.objects.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        data['name'] = ''.join(data['name'].split()).lower()
        try:
            store = Store.objects.get(name=data['name'])
        except Store.DoesNotExist:
            store = None
        if store:
            message = 'Store already exists.'
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
