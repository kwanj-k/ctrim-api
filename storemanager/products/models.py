from django.db import models

class Product(models.Model):
    name        = models.CharField(max_length=100,unique=True)
    category    = models.CharField(max_length=50)
    inventory   = models.IntegerField()
    price       = models.IntegerField()
    timestamp	= models.DateTimeField(auto_now_add=True)
    updated		= models.DateTimeField(auto_now=True)

    class Meta:
        ordering =['-updated', '-timestamp']

    def __str__(self):
        return self.name

    objects = models.Manager()
