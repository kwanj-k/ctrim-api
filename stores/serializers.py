from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Store, Staff
from users.serializers import UserSerializer

class StoreSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    name = serializers.CharField(required=True)

    def get_owner(self, obj):
        return obj.owner.username

    class Meta:
        model = Store
        fields = (
            'name',
            'owner',
        )

class StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = Staff
        fields = (
            'username',
            'email',
        )
