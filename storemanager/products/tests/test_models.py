from django.test import TestCase
from ..models import Product


class ProductTest(TestCase):
    """ Test module for Product model """

    def setUp(self):
        Product.objects.create(
            name='Monster', category='drink', inventory=20, price=165)
        Product.objects.create(
            name='Muffin', category='drink', inventory=20, price=165)

    def test_product_creation(self):
        monster = Product.objects.get(name='Monster')
        muffin = Product.objects.get(name='Muffin')
        self.assertEqual(monster.name,'Monster')
        self.assertEqual(muffin.name,'Muffin')