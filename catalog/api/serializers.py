from rest_framework import serializers
from ..models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "image", "children"]

    def get_children(self, obj):
        return CategorySerializer(obj.children.all(), many=True).data


# --- Product ---

class CategoryProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategoryProductSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "description",
            "price",
            "stock",
            "image",
            "is_available",
            "is_active",
            "created_at",
            "updated_at",
            "category",
        ]

