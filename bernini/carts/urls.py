from rest_framework import routers
from django.urls import path, include
from carts.views import UserCartViewSet

router = routers.DefaultRouter()
router.register(r'carts', UserCartViewSet)

urlpatterns = [
    path('', include((router.urls, 'carts'))),
]