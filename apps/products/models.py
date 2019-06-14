from django.db import models
from apps.common.models import AbstractBase
from apps.users.models import User
from django.db.models.signals import pre_save
from apps.common.utils import unique_slug_generator
from django.urls import reverse


class Product(AbstractBase):
    """
    Product Model
    Defines attributes of a product
    """
    name = models.CharField(max_length=100, unique=True)
    category = models.CharField(max_length=50)
    inventory = models.IntegerField()
    price = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('details', kwargs={self.name: self.slug})


def s_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(s_pre_save_receiver, sender=Product)
