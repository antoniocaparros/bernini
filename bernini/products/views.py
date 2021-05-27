from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response

from products.models import Product
from products.serializers import ProductSerializer
from carts.models import Cart, ItemCart

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'add_to_cart':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def add_to_cart(self, request, pk=None):
        """Add product to cart"""
        try:
            user = request.user
            cart = Cart.objects.get(pk=user.pk)
        except Cart.DoesNotExist as e:
            cart = Cart(user=user)
            cart.save()
        
        self.object = self.get_object()
        item = ItemCart(cart=cart, product=self.object)
        item.save()

        return Response(status=status.HTTP_200_OK, data={'message':'product added'})