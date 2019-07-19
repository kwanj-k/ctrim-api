from rest_framework.generics import (
    ListCreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
    GenericAPIView
)
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

from .models import Store
from .serializers import StoreSerializer, StoreAnalysisSerializer
from apps.helpers.store import user_stores
from apps.stock.models import Stock


class StoreListCreateView(ListCreateAPIView):
    serializer_class = StoreSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        queryset = user_stores(request)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer_context = {
            'request': request,
            'owner': request.user
        }
        data = request.data
        serializer = self.serializer_class(
            data=data, context=serializer_context)
        stores = Store.objects.all()
        new_store_name = ''.join(self.request.data['name'].split()).lower()
        for store in stores:
            if store.owner == self.request.user:
                name = ''.join(store.name.split()).lower()
                if name == new_store_name:
                    message = 'Store already exists.'
                    return Response(message, status=status.HTTP_400_BAD_REQUEST)
        serializer.is_valid(raise_exception=True)
        serializer.save(owner=self.request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class UpdateDestroyStoreView(UpdateAPIView, DestroyAPIView):
    serializer_class = StoreSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Store.objects.all()

    def get(self, request, *args, **kwargs):
        try:
            store = Store.objects.get(name=kwargs['storename'])
        except Store.DoesNotExist:
            message = 'Store does not exist'
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(
            instance=store,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


def get_stock(**kwargs):
    try:
        store = Store.objects.get(name=kwargs['storename'])
    except Store.DoesNotExist:
        message = 'Store does not exist'
        return Response(message, status=status.HTTP_404_NOT_FOUND)
    queryset = Stock.objects.filter(
        store=store
    )
    return queryset

class StoreAnalysis(GenericAPIView):
    serializer_class = StoreAnalysisSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        stock = get_stock(**kwargs)
        if len(stock) < 2:
            message = 'Take stock atleast twice to get analysis'
            return Response(message, status=status.HTTP_400_BAD_REQUEST)
        sales = []
        total_worth = 0
        for s in stock:
            k  = {
            'month': s.period,
            'amount': s.net_worth
            }
            total_worth += s.net_worth
            sales.append(k)
        current_sales = stock[0].net_worth - stock[1].net_worth
        current_net = stock[0].net_worth
        instance = {
            'current_net': current_net,
            'percentage_net_change': current_sales / total_worth,
            'current_sales': current_sales,
            'percentage_sales_change': current_sales / total_worth,
            'current_profit': current_sales - stock[0].net_worth,
            'percentage_profit_change': current_sales / total_worth,
            'sales':sales
        }
        serializer = self.serializer_class(
            context={'request': request},
            instance=instance
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
        




# class StaffListCreateView(ListCreateAPIView):
#     serializer_class = StaffSerializer
#     queryset = Staff.objects.all()
#     permission_classes = (
#         IsAuthenticated,
#     )

#     def create(self, request, slug, *args, **kwargs):
#         serializer_context = {
#             'request': request,
#             'store': get_object_or_404(Store, name=self.kwargs["slug"])
#         }
#         store = Store.objects.filter(name=slug).first()
#         if store.owner.username != request.user.username:
#             message = {"error": "You are not allowed to add staff"}
#             return Response(message, status.HTTP_403_FORBIDDEN)
#         data = request.data
#         serializer = self.serializer_class(
#             data=data, context=serializer_context)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(store_id=store.pk)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

#     def get(self, request, slug, *args, **kwargs):
#         store = Store.objects.filter(name=slug).first()
#         if not store:
#             message = {"error": "Store doesn't exist"}
#             return Response(message, status.HTTP_404_NOT_FOUND)
#         staff = store.staff.all()
#         serializer = self.serializer_class(staff, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
