import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from ..models import Product
from ..serializers import ProductSerializer


# initialize the APIClient app
client = Client()

class ProductGetAllViewsTest(TestCase):
    """ Test module for GET all products API """
    
    def setUp(self):
        Product.objects.create(
            name='Monster', category='drink', inventory=20, price=165)
        Product.objects.create(
            name='Muffin', category='drink', inventory=20, price=165)

    def test_get_all_products(self):
        # get API response
        response = client.get(reverse('list'))
        # get data from db
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DetailTest(TestCase):
    """ Test module for GET single product API """

    def setUp(self):
        self.monster = Product.objects.create(
            name='Muffin2wwww', category='drinkww', inventory=201, price=1651)

    def test_get_valid_single_product(self):
        response = client.get(
            reverse('details', kwargs={'pk': self.monster.pk}))
        product = Product.objects.get(pk=self.monster.pk)
        serializer = ProductSerializer(product)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_product(self):
        response = client.get(
            reverse('details', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class AddNewProductTest(TestCase):
    """ Test module for inserting a new product """

    def setUp(self):
        self.valid_payload = {
            'name': 'foood',
            'category': 'cake',
            'inventory': 4,
            'price': 300
        }
        self.invalid_payload = {
            'name': '',
            'category': 'cake',
            'invetory': 4,
            'price': 300
        }

    def test_create_valid_product(self):
        response = client.post(
            reverse('list'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_product(self):
        response = client.post(
            reverse('list'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdateSingleProductTest(TestCase):
    """ Test module for updating an existing product record """

    def setUp(self):
        self.monster = Product.objects.create(
            name='Muffin2wwww', category='drinkww', inventory=201, price=1651)
        self.valid_payload = {
            'name': 'foood',
            'category': 'cake',
            'inventory': 4,
            'price': 300
        }
        self.invalid_payload = {
            'name': '',
            'category': 'cake',
            'invetory': 4,
            'price': 300
        }

    def test_valid_update_product(self):
        response = client.put(
            reverse('details', kwargs={'pk': self.monster.pk}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_product(self):
        response = client.put(
            reverse('details', kwargs={'pk': self.monster.pk}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class DeleteSingleProductTest(TestCase):
    """ Test module for deleting an existing product record """

    def setUp(self):
        self.monster = Product.objects.create(
            name='Muffin2wwww', category='drinkww', inventory=201, price=1651)

    def test_valid_delete_product(self):
        response = client.delete(
            reverse('details', kwargs={'pk': self.monster.pk}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_invalid_delete_product(self):
        response = client.delete(
            reverse('details', kwargs={'pk': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)