from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import Store
from .serializers import StoreSerializer


class StoreListCreateView(ListCreateAPIView):
    serializer_class = StoreSerializer
    queryset = Store.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
