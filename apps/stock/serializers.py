from rest_framework import serializers
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    """Product Model Serializer"""

    class Meta:
        """Access fields and create returned object."""
        model = Product
        exclude = ('deleted',)
        read_only_fields = ('updated_at','created_at', 'id')


class PackageSerializer(serializers.ModelSerializer):
    """Package Model Serializer"""

    class Meta:
        """Access fields and create returned object."""
        model = Package
        exclude = ('deleted',)
        read_only_fields = ('updated_at','created_at', 'id')


class StockSerializer(serializers.ModelSerializer):
    """Stock Model Serializer"""

    class Meta:
        """Access fields and create returned object."""
        model = Stock
        exclude = ('deleted',)
        read_only_fields = ('updated_at','created_at', 'id')


class StockProductSerializer(serializers.ModelSerializer):
    """StockProduct Model Serializer"""

    class Meta:
        """Access fields and create returned object."""
        model = StockProduct
        exclude = ('deleted',)
        read_only_fields = ('updated_at','created_at', 'id')
