from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Store
from users.serializers import UserSerializer

class StoreSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    staff = UserSerializer(many=True, read_only=True)
    name = serializers.CharField(required=True)

    def get_owner(self, obj):
        return obj.owner.username

    class Meta:
        model = Store
        fields = (
            'name',
            'owner',
            'staff'
        )
