from django.core.mail import EmailMessage
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response

from carts.models import Cart, ItemCart
from carts.permissions import IsCartOwner
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

    def get_permissions(self):
        if self.action == 'create' or self.action == 'list':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsCartOwner]

        return [permission() for permission in permission_classes]

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

    @action(detail=True, methods=['get'], permission_classes=[IsAuthenticated])
    def make_order(self, request, pk=None):
        if str(request.user.pk) == str(pk):
            items_in_cart = ItemCart.objects.filter(cart__pk=pk)
            csv = ""
            for itemcart in items_in_cart:
                csv += str(itemcart.product.id) + "," + str(itemcart.product.title) + "," + str(itemcart.product.price) + "\n"
            
            email = EmailMessage(
                'Pedido por el usuario ' + str(request.user.email),
                'Se adjunta el CSV con el pedido :)',
                'admin@admin.com',
                ['' + str(request.user.email) + ''],
                ['' + str(request.user.email) + ''],
                reply_to=['admin@admin.com'],
                headers={},
            )
            email.attach('pedido.csv', csv, 'text/csv')
            email.send()
            
            # borramos el carrito
            cart = Cart.objects.get(pk=pk) # esto no puede petar, creo..
            cart.delete()
            
            return Response({'status': 'make_order correct. CSV sended.'})
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)