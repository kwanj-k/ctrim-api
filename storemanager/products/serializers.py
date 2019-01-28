from rest_framework import serializers
from django.http import JsonResponse
from .models import Product
from django.utils.text import slugify
from taggit_serializer.serializers import (TagListSerializerField,
                                           TaggitSerializer)


class ProductSerializer(TaggitSerializer,serializers.ModelSerializer):
    category = serializers.CharField(required=False)
    owner = serializers.SerializerMethodField(read_only=True)
    url = serializers.HyperlinkedIdentityField(
        read_only=True,
        lookup_field='slug',
        view_name='details'
    )
    tagList = TagListSerializerField()

    def get_owner(self, obj):
        user = obj.owner.username
        return user


    class Meta:
        model = Product
        fields = (
            'id', 'name', 'category', 'inventory', 'price', 'owner',
            'updated_at', 'created_at', 'url', 'tagList'
        )
        read_only_fields = ('updated_at', 'created_at', 'slug',)



