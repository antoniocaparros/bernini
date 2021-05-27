from rest_framework import serializers
from carts.models import Cart, ItemCart

class ItemCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemCart
        fields = ['id', 'product']

class CartSerializer(serializers.ModelSerializer):
    products = ItemCartSerializer(many=True, read_only=True)
    class Meta:
        model = Cart
        fields = ['url', 'user', 'products']

class DeleteItemCartSerializer(serializers.Serializer):
    """
    Serializer for password change endpoint.
    """
    id_product = serializers.IntegerField(
        required=True,
        help_text='id product',
        style={'input_type': 'integer', 'placeholder': 'id product'}
    )

    class Meta:
        fields = ['id_product']
