from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.hashers import make_password

from apps.users.models import User
from apps.common.models import AbstractBase


class StaffManager(BaseUserManager):

    def create_staff(self, username, email, store_id, password=None):
        phash = make_password(password)
        staff = self.model(
            username=username,
            email=email,
            store_id=store_id,
            password=phash
        )
        staff.save()
        return staff


class Store(AbstractBase):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='owner'
    )
    name = models.CharField(
        max_length=50,
        blank=False,
        null=False
    )

    def __str__(self):
        return self.name


class Staff(User):
    is_admin = models.BooleanField(default=False)
    store = models.ForeignKey(
        Store,
        related_name='staff',
        on_delete=models.CASCADE,
        null=False
    )

    objects = StaffManager()
