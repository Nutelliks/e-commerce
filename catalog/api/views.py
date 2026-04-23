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


class ProductViewSet(CacheMixin, viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(is_active=True).select_related("category")
    serializer_class = ProductSerializer
    lookup_field = "slug"
    lookup_url_kwarg = "product_slug"
    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "created_at", "name"]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        params = request.query_params.lists()
        cache_name = "products:list:" + ":".join(
            f"{k}={",".join(sorted(v))}" for k, v in sorted(params)
        )

        def builder():
            page = self.paginate_queryset(queryset)

            if page is not None:
                data = self.get_serializer(page, many=True).data
                return self.get_paginated_response(data).data

            data = self.get_serializer(queryset, many=True).data
            return data

        data = self.get_set_cache(cache_name, 60 * 15, builder)
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        builder = lambda: self.get_serializer(self.get_object()).data
        slug = self.kwargs[self.lookup_url_kwarg]
        data = self.get_set_cache(f"products:detail:{slug}", 60 * 15, builder)

        return Response(data)
