from django.contrib import admin
from .models import Category, Product


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1
    verbose_name = "Child category"
    verbose_name_plural = "Child categories"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent")
    list_filter = ("parent",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)
    inlines = (CategoryInline,)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "category", "price", "stock", "is_available")
    list_filter = ("category", "is_available", "created_at")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("price", "stock")
    readonly_fields = ("created_at",)
    fieldsets = (
        ("Main info", {"fields": ("name", "slug", "category", )}),
        (
            None,
            {"fields": ("description",)},
        ),
        ("Available", {"fields": ("price", "stock", "is_available")}),
        (None, {"fields": ("image",)}),
    )
