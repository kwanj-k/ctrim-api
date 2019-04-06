from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .models import Store, Staff
from .serializers import StoreSerializer, StaffSerializer


class StoreListCreateView(ListCreateAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class StaffListCreateView(ListCreateAPIView):
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()
    permission_classes = (IsAuthenticated,)

    def create(self, request, slug, *args, **kwargs):
        serializer_context = {
            'request': request,
            'store': get_object_or_404(Store, name=self.kwargs["slug"])
        }
        store = Store.objects.filter(name=slug).first()
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
