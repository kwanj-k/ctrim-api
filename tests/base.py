# from django.urls import reverse
# from rest_framework.test import APIClient, APITestCase


# class BaseTestCase(APITestCase):

#     def setUp(self):
#         self.client = APIClient()
#         self.signup_url = reverse('authentication:register')
#         self.login_url = reverse('authentication:login')
#         self.stores_url = reverse('stores:stores_list')
#         self.products_url = reverse('products:products_list', kwargs={"stock_id": 1})
#         self.stocks_url = reverse('stocks:stocks_list', kwargs={"store_id": 1})
#         self.signup_data = {
#                         "email": "sly@gmail.com",
#                         "password": "testpassword@123",
#                         "username": "tester"
#                         }
#         self.product_data = {
#                         "name": "Msafi 1kg Powder",
#                         "packaging": "CTN",
#                         "package_pieces": 6,
#                         "number_of_packages": 10,
#                         "package_price": 1000,
#                         "piece_price": 140,
#                         "free_pieces": 3
#                         }
#         self.store_data = {
#                         "name": "ctrim",
#                         "description": "string"
#                         }
#         self.stock_data = {
#                         "name": "stock test",
#                         "description": "string"
#                         }
    
#     def authenticate(self):
#         response = self.client.post(
#             self.signup_url,
#             self.signup_data,
#             format="json")
#         self.client.credentials(
#             HTTP_AUTHORIZATION='Bearer ' + response.data['token'])        
#         return

#     def create_store(self):
#         res = self.client.post(
#                         self.stores_url,
#                         self.store_data,
#                         format="json")
#         return res
    
#     def create_stock(self):
#         res = self.client.post(
#                         self.stocks_url,
#                         self.stock_data,
#                         format="json")
#         return res
