from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "phone", "is_active"]
    list_filter = ["is_active", "is_staff", "date_joined"]
    search_fields = ["username", "email"]
    fieldsets = (
        (
            "Personal",
            {
                "fields": ("username", "email", "first_name", "last_name", "phone"),
            },
        ),
        ("Permissions", {"fields": ("is_active", "is_staff")}),
        ("Dates", {"fields": ("date_joined", "last_login")}),
    )
    readonly_fields = ["date_joined", "last_login"]
