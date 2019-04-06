from django.db import models
from django.contrib.auth import get_user_model

from users.models import User
from common.models import AbstractBase


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
