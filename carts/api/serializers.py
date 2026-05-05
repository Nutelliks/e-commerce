from rest_framework import serializers
from ..models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "product_name",
            "quantity",
            "price_snapshot",
            "subtotal",
        ]

    def get_product_name(self, obj):
        return obj.product.name
