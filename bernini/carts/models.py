from django.db import models
from django.contrib.auth.models import User
from products.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    def __str__(self):
        return "%s cart" % self.user.username

class ItemCart(models.Model):
    id = models.BigAutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    cart = models.ForeignKey(Cart, related_name="cart", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name="product", on_delete=models.CASCADE)

    def __str__(self):
        return "%s cart has %s product" % (self.cart.user.username, self.product.title)