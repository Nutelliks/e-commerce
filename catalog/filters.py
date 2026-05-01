import django_filters
from rest_framework.exceptions import ValidationError
from .models import Product


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(method="filter_price_min", label="price_min")
    price_max = django_filters.NumberFilter(method="filter_price_max", label="price_max")

    class Meta:
        model = Product
        fields = ["category", "is_available"]

    def filter_price_min(self, queryset, name, value):
        if value < 0:
            raise ValidationError("Цена не может быть отрицательной")
        return queryset.filter(price__gte=value)

    def filter_price_max(self, queryset, name, value):
        if value < 0:
            raise ValidationError("Цена не может быть отрицательной")
        return queryset.filter(price__lte=value)

    def filter_queryset(self, queryset):
        data = self.form.cleaned_data
        min_price = data.get("price_min")
        max_price = data.get("price_max")

        if min_price is not None and max_price is not None:
            if min_price > max_price:
                raise ValidationError("Диапазон цен некорректно")

        return super().filter_queryset(queryset)
