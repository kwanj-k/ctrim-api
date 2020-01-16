from django.urls import reverse
from rest_framework.test import APIClient, APITestCase


class BaseTestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('authentication:register')
        self.login_url = reverse('authentication:login')
        self.stores_url = reverse('store:stores_list')
        self.products_url = reverse('product:products_list', kwargs={"storename": 'ctrim'})
        self.signup_data = {
                        "email": "sly@gmail.com",
                        "password": "testpassword@123",
                        "confirm_password": "testpassword@123",
                        "username": "tester"
                        }
        self.product_data = {
                        "name": "Msafi 1kg Powder",
                        "packaging": "CTN",
                        "package_pices": 6,
                        "number_of_packages": 10,
                        "package_price": 1000,
                        "piece_price": 140,
                        "number_of_pieces": 3
                        }
        self.store_data = {
                        "name": "ctrim",
                        "description": "string"
                        }
    
    def authenticate(self):
        response = self.client.post(self.signup_url, self.signup_data,
                                    format="json")
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['token'])        
        return

    def create_store(self):
        res = self.client.post(self.stores_url, self.store_data,
                                    format="json")
        return res
