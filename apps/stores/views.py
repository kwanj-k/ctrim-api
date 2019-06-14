from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .models import Store, Staff
from .serializers import StoreSerializer, StaffSerializer
from apps.helpers.store import user_stores


class StoreListCreateView(ListCreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = user_stores(request)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class GetUpdateDestroyStoreView(RetrieveUpdateDestroyAPIView):
    serializer_class = StoreSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Store.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            store = Store.objects.get(pk=kwargs['pk'])
        except Store.DoesNotExist:
            message = 'Store does not exist'
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            instance=store,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class StaffListCreateView(ListCreateAPIView):
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()
    permission_classes = (
        IsAuthenticated,
    )

    def create(self, request, slug, *args, **kwargs):
        serializer_context = {
            'request': request,
            'store': get_object_or_404(Store, name=self.kwargs["slug"])
        }
        store = Store.objects.filter(name=slug).first()
        if store.owner.username != request.user.username:
            message = {"error": "You are not allowed to add staff"}
            return Response(message, status.HTTP_403_FORBIDDEN)
        data = request.data
        serializer = self.serializer_class(
            data=data, context=serializer_context)
        serializer.is_valid(raise_exception=True)
        serializer.save(store_id=store.pk)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, slug, *args, **kwargs):
        store = Store.objects.filter(name=slug).first()
        if not store:
            message = {"error": "Store doesn't exist"}
            return Response(message, status.HTTP_404_NOT_FOUND)
        staff = store.staff.all()
        serializer = self.serializer_class(staff, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
