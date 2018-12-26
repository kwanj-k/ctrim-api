from django.db import models
from common.models import AbstractBase
from users.models import User
from django.conf import settings
import uuid

class Product(AbstractBase):
    """
    Product Model
    Defines attributes of a product
    """
    name = models.CharField(max_length=100,unique=True)
    category = models.CharField(max_length=50)
    inventory = models.IntegerField()
    price = models.IntegerField()
    owner = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
