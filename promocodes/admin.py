from django.contrib import admin
from django.contrib import messages
from .models import PromoCode


@admin.action(description="Activate selected promocodes")
def activate_promocodes(modeladmin, request, queryset):
    updated = queryset.update(is_active=True)
    modeladmin.message_user(
        request,
        f"{updated} промокодов активировано",
        messages.SUCCESS
    )

@admin.action(description="Deactivate selected promocodes")
def deactivate_promocodes(modeladmin, request, queryset):
    updated = queryset.update(is_active=False)
    modeladmin.message_user(
        request,
        f"{updated} промокодов деактивировано",
        messages.SUCCESS
    )


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    actions = (activate_promocodes, deactivate_promocodes)
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
    ordering = ("-valid_to", "-id",)
    search_fields = ("code",)
    readonly_fields = ("used_count", "id")
    filter_horizontal = ("users",)
