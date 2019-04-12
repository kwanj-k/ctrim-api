from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Store, Staff
from users.serializers import UserSerializer
from users.models import User


class StoreSerializer(serializers.ModelSerializer):
    owner = serializers.SerializerMethodField()
    name = serializers.CharField(required=True)
    pk = serializers.IntegerField(required=False)

    def get_owner(self, obj):
        return obj.owner.username

    class Meta:
        model = Store
        fields = (
            'name',
            'owner',
            'pk'
        )

class StaffSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = Staff
        fields = (
            'username',
            'email',
            'password',
        )

    def create(self, validated_data):
        #import pdb; pdb.set_trace()
        return Staff.objects.create_staff(**validated_data)
