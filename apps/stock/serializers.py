from rest_framework import serializers
from .models import Stock
from apps.products.serializers import ProductSerializer


class StockSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    net_worth = serializers.SerializerMethodField()
    store = serializers.SerializerMethodField()

    def get_store(self, obj):
        return obj.store.name

    def get_net_worth(self, obj):
        net = 0
        products = obj.products.all()
        for product in products:
            net += product.number_of_packages * product.package_price
            net += product.number_of_pieces * product.piece_price
        return net

    class Meta:
        model = Stock
        exclude = ('deleted', 'active',)
        read_only_fields = ('updated_at','created_at')
    
    def to_internal_value(self, value):
        return value
