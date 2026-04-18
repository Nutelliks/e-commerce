from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
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
    
    @method_decorator(cache_page(60 * 15))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @method_decorator(cache_page(60 * 15))
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
