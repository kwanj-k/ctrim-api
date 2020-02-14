from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Store
from apps.users.serializers import UserSerializer
from apps.users.models import User


class StoreSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    pk = serializers.IntegerField(read_only=True)


    class Meta:
        model = Store
        fields = (
            'name',
            'description',
            'pk'
        )
