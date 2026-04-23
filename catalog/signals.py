from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Category, Product


@receiver([post_delete, post_save], sender=Category)
def delete_categories_cache(sender, instance, **kwargs):
    cache.delete("categories:list")
    cache.delete(f"categories:detail:{instance.slug}")
    if instance.parent is not None:
        cache.delete(f"categories:detail:{instance.parent.slug}")


@receiver([post_delete, post_save], sender=Product)
def delete_products_cache(sender, instance, **kwargs):
    cache.delete_pattern("products:list:*")
    cache.delete(f"products:detail:{instance.slug}")