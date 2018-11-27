from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(required=False)
    class Meta:
        model = Product
        fields = ('id', 'name', 'category', 'inventory', 'price')
    
    # id          = serializers.IntegerField(read_only=True)
    # name        = serializers.CharField(required=True, allow_blank=False, max_length=100)
    # category    = serializers.CharField(required=False, allow_blank=True, max_length=50)
    # inventory   = serializers.IntegerField(required=True,all_blank= False)
    # price       = serializers.IntegerField(required=True,all_blank= False)
