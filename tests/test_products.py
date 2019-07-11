from rest_framework.views import status

from .base import BaseTestCase

class ProductsTestCase(BaseTestCase):

    def test_create_product(self):
        self.authenticate()
        self.create_store()
        response = self.client.post(self.products_url, self.product_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
