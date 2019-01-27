from rest_framework import serializers
from django.http import JsonResponse
from .models import Product, Tag
from django.utils.text import slugify


class TagField(serializers.RelatedField):
    queryset = Tag.objects.all()

    def to_internal_value(self, data):
        tag, created = Tag.objects.get_or_create(tag=data, slug=slugify(data))

        return tag

    def to_representation(self, value):
        return value.tag



class TagSerializer(serializers.ModelSerializer):
    tag = serializers.CharField(
        required=True,
        max_length=28,
        allow_blank=False,
        allow_null=False,
        error_messages={
            "blank": "Please specify a tag",
            "required": "Please specify a tag",
            "max_length": "Tag cannot be more than 28 characters"
        })
    slug = serializers.SlugField(read_only=True)

    class Meta:
        model = Tag
        fields = ['tag', 'slug']

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField(required=False)
    owner = serializers.SerializerMethodField()
    url = serializers.HyperlinkedIdentityField(
        read_only=True,
        lookup_field='slug',
        view_name='details'
    )
    tags = TagField(
        many=True,
        required=False,
        error_messages={'not_a_list': "The tags must be a list of strings"})

    def get_owner(self, obj):
        user = obj.owner.username
        return user

    def create(self, validated_data):

        tags = validated_data.pop('tags', [])

        product = Product.objects.create(**validated_data)

        for tag in tags:
            product.tags.add(tag)
        return product

    def update(self, instance, validated_data):

        tags = validated_data.pop('tags', [])

        instance.tags.clear()
        for tag in tags:
            instance.tags.add(tag)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance

    class Meta:
        model = Product
        fields = (
            'id', 'name', 'category', 'inventory', 'price', 'owner',
            'updated_at', 'created_at', 'url', 'tags'
        )
        read_only_fields = ('updated_at', 'created_at', 'slug',)



