from rest_framework import viewsets
from .serializers import CategorySerializer
from ..models import Category


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer