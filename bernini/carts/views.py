from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from carts.models import Cart, ItemCart
from carts.serializers import CartSerializer, ItemCartSerializer, DeleteItemCartSerializer
from products.models import Product

class CartViewSet(viewsets.ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class ItemCartViewSet(viewsets.ModelViewSet):
    queryset = ItemCart.objects.all()
    serializer_class = ItemCartSerializer
    permissions = [IsAuthenticated]

class UserCartViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

    def get_serializer_class(self):
        if self.action == 'delete_product':
            return DeleteItemCartSerializer      
        return CartSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def delete_product(self, request, pk=None):
        serializer = DeleteItemCartSerializer(data=request.data)
        if serializer.is_valid():
            try:
                product = Product.objects.get(pk=serializer.validated_data['id_product'])
                cart = Cart.objects.get(pk=pk)
            except Product.DoesNotExist:
                return Response({'status': 'Product does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            except Cart.DoesNotExist:
                return Response({'status': 'Cart does not exist'}, status=status.HTTP_400_BAD_REQUEST)
            
            items = ItemCart.objects.filter(product=product, cart=cart)
            if len(items) == 0:
                return Response({'status':'The item does not exist in the cart'}, status=status.HTTP_400_BAD_REQUEST)
            item = items[0]
            item.delete()
            return Response({'status': 'item deleted'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)