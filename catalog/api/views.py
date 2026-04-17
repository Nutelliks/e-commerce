from rest_framework import viewsets
from django.db.models import Prefetch
from .serializers import CategorySerializer
from ..models import Category


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True).prefetch_related(
        Prefetch("children", queryset=Category.objects.filter(is_active=True))
    )
    serializer_class = CategorySerializer
    lookup_field = "slug"
    lookup_url_kwarg = "category_slug"

    def get_queryset(self):
        if self.action == "list":
            return self.queryset.filter(parent=None)
        return self.queryset
