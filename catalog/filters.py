import django_filters
from django.core.exceptions import ValidationError
from .models import Product


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte", method="price_validation")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte", method="price_validation")

    class Meta:
        model = Product
        fields = ["category", "is_available"]


    def filter_queryset(self, queryset):
        min_price = self.data.get("price_min")
        max_price = self.data.get("price_max")

        if min_price < 0 or max_price < 0:
            return ValidationError("Цена не может быть отрицательным числом")
        if float(max_price) < float(min_price):
            return ValidationError("Максимальная цена не может быть ниже минимальной цены")

        return super().filter_queryset(queryset)