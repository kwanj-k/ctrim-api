from django.db import models
from apps.common.models import AbstractBase
from apps.products.models import Product
from apps.stores.models import Store

class Stock(AbstractBase):
    products = models.ManyToManyField(Product, verbose_name='list of products')
    period = models.CharField(max_length=50)
    net_worth = models.FloatField()
    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name='stock')
        
    def __str__(self):
        return self.period  
