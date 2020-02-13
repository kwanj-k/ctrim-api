from django.db import models

from apps.common.models import AbstractBase


class Store(AbstractBase):
    name = models.CharField(
        max_length=50,
        blank=False,
        null=False
    )
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
