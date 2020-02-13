from rest_framework import serializers
from .models import Stock
from apps.products.serializers import ProductSerializer


class StockSerializer(serializers.ModelSerializer):
    store = serializers.SerializerMethodField()

    def get_store(self, obj):
        return obj.store.name

    class Meta:
        model = Stock
        exclude = ('deleted', 'active',)
        read_only_fields = ('updated_at','created_at')
