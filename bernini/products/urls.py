from rest_framework import routers
from django.urls import path, include
from products.views import ProductViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include((router.urls, 'products'))),
]