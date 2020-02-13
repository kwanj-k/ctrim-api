from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Store
from .serializers import StoreSerializer


class StoreListCreateView(ListCreateAPIView):
    """ List/Create stores"""
    serializer_class = StoreSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Store.objects.all()
