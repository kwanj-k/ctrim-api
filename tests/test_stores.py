# from rest_framework.views import status

# from .base import BaseTestCase

# class StoresTestCase(BaseTestCase):

#     def test_create_store(self):
#         self.authenticate()
#         response = self.client.post(self.stores_url, self.store_data,
#                                     format="json")
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_get_stores(self):
#         self.authenticate()
#         self.client.post(self.stores_url, self.store_data,
#                                     format="json")
#         response = self.client.get(self.stores_url, format="json")
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_create_existing_store(self):
#         self.authenticate()
#         self.client.post(self.stores_url, self.store_data,
#                                     format="json")
#         response = self.client.post(self.stores_url, self.store_data,
#                                     format="json")
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
