from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    store = serializers.SerializerMethodField()

    def get_store(self,obj):
        return obj.store.name

    class Meta:
        model = Product
        exclude = ('deleted', 'active',)
        read_only_fields = ('updated_at','created_at', 'product_worth')
