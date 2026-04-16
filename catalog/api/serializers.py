from rest_framework import serializers
from ..models import Category


class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "image"]


    def get_subcategories(self, obj):
        return obj.children.filter(is_active=True)