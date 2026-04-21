from rest_framework import viewsets
from rest_framework.response import Response
from django.db.models import Prefetch
from common.mixins import CacheMixin
from .serializers import CategorySerializer, ProductSerializer
from ..models import Category, Product
from ..filters import ProductFilter


class CategoryViewSet(CacheMixin, viewsets.ReadOnlyModelViewSet):
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

    def list(self, request, *args, **kwargs):
        builder = lambda: self.get_serializer(self.get_queryset(), many=True).data
        data = self.get_set_cache("categories:list", 60 * 15, builder)

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        builder = lambda: self.get_serializer(self.get_object()).data
        slug = self.kwargs[self.lookup_url_kwarg]
        data = self.get_set_cache(f"categories:detail:{slug}", 60 * 15, builder)

        return Response(data)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at", "name"]