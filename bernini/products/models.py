from django.db import models
from .validators import validate_price

class Product(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(default='')
    price = models.FloatField(validators=[validate_price])

