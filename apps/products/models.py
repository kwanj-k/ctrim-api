from django.db import models

from apps.common.models import AbstractBase
from apps.stock.models import Stock

class Product(AbstractBase):
    """
    Product Model
    Defines attributes of a product
    """
    name = models.CharField(max_length=100)
    packaging = models.CharField(max_length=20)
    package_pieces = models.IntegerField()
    number_of_packages = models.IntegerField()
    package_price = models.IntegerField()
    piece_price = models.IntegerField()
    free_pieces = models.IntegerField()
    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name='products')

    def __str__(self):
        return self.name

    class Meta:
        """Define metadata options."""

        unique_together = ['stock', 'name']
