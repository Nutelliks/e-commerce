from django.contrib import admin
from .models import PromoCode


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "discount_type",
        "discount_value",
        "max_uses",
        "used_count",
        "is_active",
        "valid_from",
        "valid_to",
    )
    list_filter = (
        "is_active",
        "discount_type",
        "once_per_user",
        "valid_from",
        "valid_to",
    )
    ordering = ("-id",)
    search_fields = ("code",)
    readonly_fields = ("used_count",)
    filter_horizontal = ("users",)
