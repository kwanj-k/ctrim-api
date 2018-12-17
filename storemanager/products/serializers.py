from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(required=False)
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'inventory', 'price')
