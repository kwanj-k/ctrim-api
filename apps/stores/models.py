from django.db import models

from apps.common.models import AbstractBase
from apps.users.models import User


class Store(AbstractBase):
    name = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        unique=True,
    )
    owner = models.ForeignKey(
        User, on_delete=models.DO_NOTHING,
        related_name='stocks')
    description = models.CharField(
        max_length=200, blank=True, null=True
    )

    def __str__(self):
        return self.name
