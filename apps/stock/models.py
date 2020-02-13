from django.db import models
from apps.common.models import AbstractBase
from apps.products.models import Product
from apps.stores.models import Store

class Stock(AbstractBase):
    name = models.CharField(max_length=50)
    stock_type = models.CharField(max_length=50, default='monthly')
    description = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='stock'
    )
        
    def __str__(self):
        return self.name  
