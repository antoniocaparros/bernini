from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

class ProductAPIViewTestCase(APITestCase):
    url = reverse("product-list")

    def setUp(self):
        userAdmin = User.objects.create_user("admin", "admin")
        userAdmin.is_staff = True
        userAdmin.save()
        self.token = Token.objects.get_or_create(user=userAdmin)

    def test_list_products(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.data['results'])
    
    def test_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token[0]))
        response = self.client.post(self.url, data={'title': 'product 1', 'description':'product 1 description', 'price': 10.1}, format='json')
        self.assertEqual(201, response.status_code)
    