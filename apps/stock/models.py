from django.db import models

from apps.common.models import AbstractBase, CapitalizeField
from apps.stores.models import Store


class Package(AbstractBase):
    """
    Defines attributes of a package
    """
    name = CapitalizeField(max_length=100)
    number_of_items = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.name


class Product(AbstractBase):
    """
    Defines attributes of a product
    """
    name = CapitalizeField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Stock(AbstractBase):
    """
    Defines attributes of a Stock
    """
    TYPES = (
        ('daily', 'DAILY'),
        ('weekly', 'WEEKLY'),
        ('monthly', 'MONTHLY'),
    )
    ref_number = models.CharField(max_length=255, unique=True)
    stock_type = models.CharField(
        max_length=50, 
        default='monthly',
        choices=TYPES
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.DO_NOTHING,
        related_name='stocks'
    )
        
    def __str__(self):
        return self.ref_number  


class StockProduct(AbstractBase):
    """
    Defines attributes of a StockProduct
    """
    stock = models.ForeignKey(
        Stock, related_name='stock', on_delete=models.DO_NOTHING)
    product = models.ForeignKey(
        Product, related_name='stock_products', on_delete=models.DO_NOTHING)
    packaging = models.ForeignKey(
        Package, related_name='stock_product_packaging', on_delete=models.DO_NOTHING)
    quantity = models.FloatField()

    def __str__(self):
        return self.product.name
    
    class Meta:
        unique_together = ['stock', 'product']
