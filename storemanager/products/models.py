from django.db import models

class Product(models.Model):
    """
    Product Model
    Defines attributes of a product
    """
    name        = models.CharField(max_length=100,unique=True)
    category    = models.CharField(max_length=50)
    inventory   = models.IntegerField()
    price       = models.IntegerField()
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering =['-updated_at', '-created_at']

    def __str__(self):
        return self.name

    objects = models.Manager()
