from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from products.models import Product
from products.views import ProductViewSet

class ProductAPIViewTestCase(APITestCase):
    url = reverse("product-list")

    def setUp(self):
        userAdmin = User.objects.create_user("admin", "admin")
        userAdmin.is_staff = True
        userAdmin.save()
        self.userAdmintoken = Token.objects.get_or_create(user=userAdmin)

    def test_list_products(self):
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        self.assertEqual([], response.data['results'])
    
    def test_create_product(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.userAdmintoken[0]))
        response = self.client.post(self.url, data={'title': 'product 1', 'description':'product 1 description', 'price': 10.1}, format='json')
        self.assertEqual(201, response.status_code)
    
    def add_cart(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.userAdmintoken[0]))
        response = self.client.post(self.url, data={'title': 'product 1', 'description':'product 1 description', 'price': 10.1}, format='json')
        self.assertEqual(200, response.status_code)

class ProductAddCartAPIViewTestCase(APITestCase):
    url = reverse("product-add_to_cart", args=[1])
    url_cart = reverse("cart-detail", args=[1])
    

    def setUp(self):
        userAdmin = User.objects.create_user("admin", "admin")
        userAdmin.is_staff = True
        userAdmin.save()
        self.userAdmintoken = Token.objects.get_or_create(user=userAdmin)
        product = Product.objects.create(title="product 1", description="product 1 description", price=10.2)
        product.save()
    
    def test_product_add_to_cart(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.userAdmintoken[0]))
        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)
        response_cart = self.client.get(self.url_cart)
        self.assertEqual(True, "product 1" in str(response_cart.content))
