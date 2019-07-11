from rest_framework.views import status

from .base import BaseTestCase

class UsersTestCase(BaseTestCase):

    def test_register_user(self):
        """tests that a user can be registered"""
        response = self.client.post(self.signup_url, self.signup_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('username', response.data)
        self.assertIn('email', response.data)
        self.assertIn('token', response.data)

    def test_login_user(self):
        """tests that a user can be logged in"""
        self.client.post(self.signup_url, self.signup_data,
                                    format="json")
        response = self.client.post(self.login_url, self.signup_data,
                                    format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
