from rest_framework import serializers
from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "image", "subcategories"]


    def get_subcategories(self, obj):
        children = obj.children.filter(is_active=True)
        return CategorySerializer(children, many=True).data