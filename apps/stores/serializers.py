from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Store
from apps.users.serializers import UserSerializer
from apps.users.models import User


class StoreSerializer(serializers.ModelSerializer):
    """Stores model serializer."""

    class Meta:
        model = Store
        exclude = ('deleted',)
        read_only_fields = ('id','updated_at','created_at', 'owner',)
