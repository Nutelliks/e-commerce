from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Category


@receiver([post_delete, post_save], sender=Category)
def delete_categories_cache(sender, instance, **kwargs):
    cache.delete("categories:list")
    cache.delete(f"categories:detail:{instance.slug}")
    cache.delete(f"categories:detail:{instance.parent.slug}")