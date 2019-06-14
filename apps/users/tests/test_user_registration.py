from django.urls import reverse
from rest_framework.views import status
from rest_framework.test import APIClient, APITestCase


class RegistrationTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = reverse('authentication:register')
        self.signup_data = {
                            "email": "test@gmail.com",
                            "password": "testpassword@123",
                            "username": "tester"
                        }

    def test_register_user(self):
        """tests that a user can be registered"""
        response = self.client.post(self.signup_url, self.signup_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('token', response.data)
