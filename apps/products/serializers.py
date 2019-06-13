from rest_framework import serializers
from django.http import JsonResponse
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(required=False)
    owner = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(read_only=True,
                            lookup_field='slug',
                            view_name='details')
    def get_owner(self,obj):
        user = obj.owner.username
        return user
    class Meta:
        model = Product
        fields = [
            'id','name','category','inventory','price','owner',
            'updated_at','created_at','slug','url'
        ]
        read_only_fields = ('updated_at','created_at','slug')
