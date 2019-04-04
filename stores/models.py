from django.db import models

# Create your models here.
from django.db import models

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
    staff = models.ManyToManyField(User)

    def __str__(self):
        return self.name
