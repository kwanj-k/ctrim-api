from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    stock = serializers.SerializerMethodField()

    def get_stock(self,obj):
        return obj.stock.name

    class Meta:
        model = Product
        exclude = ('deleted', 'active',)
        read_only_fields = ('updated_at','created_at', 'stock')
