from rest_framework import serializers
from ..models import CartItem, Cart


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
            "get_subtotal",
        ]

    def get_product_name(self, obj):
        return obj.product.name
    

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)
    
    class Meta:
        model = Cart
        fields = ("id", "items", "get_total_price", "get_items_count")
