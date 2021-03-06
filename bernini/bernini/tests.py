from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase

class UserRegisterAPIViewTestCase(APITestCase):
    url = reverse("user-list")

    def setUp(self):
        self.username = "duplicate"
        self.email = "duplicate@example.com"
        self.password = "duplicate"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_register_without_username(self):
        response = self.client.post(self.url, {"password": self.password})
        self.assertEqual(400, response.status_code)

    def test_register_without_password(self):
        response = self.client.post(self.url, {"username": self.username})
        self.assertEqual(400, response.status_code)

    def test_register_with_wrong_email(self):
        response = self.client.post(self.url, {"username": self.username, "email": "baskahsd", "password": self.password})
        self.assertEqual(400, response.status_code)

    def test_register_duplicate(self):
        response = self.client.post(self.url, {"username": self.username, "email": self.email, "password": self.password})
        self.assertEqual(400, response.status_code)
    
    def test_register_correct(self):
        response = self.client.post(self.url, {"username": "admin", "email": "admin@example.com", "password": "admin"})
        self.assertEqual(201, response.status_code)

class UserLoginAPIViewTestCase(APITestCase):
    url = reverse("api_token_auth")

    def setUp(self):
        self.username_correct = "admin"
        self.password_correct = "admin"
        self.email = "admin@admin.com"
        self.username_incorrect = "admin2"
        self.password_incorrect = "admin2"
        self.user = User.objects.create_user(self.username_correct, self.email, self.password_correct)

    def test_login_incorrect(self):
        response = self.client.post(self.url, {"username": self.username_correct , "password": self.password_incorrect})
        self.assertEqual(400, response.status_code)

    def test_register_login_correct(self):
        response = self.client.post(self.url, {"username": self.username_correct , "password": self.password_correct})
        self.assertEqual(200, response.status_code)

