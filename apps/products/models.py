from django.db import models
from apps.common.models import AbstractBase
from apps.stores.models import Store

class Product(AbstractBase):
    """
    Product Model
    Defines attributes of a product
    """
    name = models.CharField(max_length=100, unique=True)
    packaging = models.CharField(max_length=20)
    package_pices = models.IntegerField()
    number_of_packages = models.IntegerField()
    package_price = models.IntegerField()
    piece_price = models.IntegerField()
    number_of_pieces = models.IntegerField()
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='store')

    def __str__(self):
        return self.name
