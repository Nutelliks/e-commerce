from django.contrib import admin
from .models import Category, Product


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 1
    verbose_name = "Child category"
    verbose_name_plural = "Child categories"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "parent", "is_active", "created_at")
    list_filter = ("is_active", "parent", "created_at")
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    ordering = ("name",)
    list_editable = ("is_active", )
    inlines = (CategoryInline,)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "category", "price", "stock", "is_available")
    list_filter = ("category", "is_available", "created_at")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_editable = ("price", "stock")
    readonly_fields = ("created_at", "updated_at")
    fieldsets = (
        ("Main info", {"fields": ("name", "slug", "category", )}),
        (
            None,
            {"fields": ("description",)},
        ),
        ("Available", {"fields": ("price", "stock", "is_available")}),
        (None, {"fields": ("image",)}),
        ("Meta", {"fields": ("created_at", "updated_at")}),
    )
