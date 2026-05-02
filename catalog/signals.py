from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Category, Product

import logging

catalog_logger = logging.getLogger(__name__)


@receiver([post_delete, post_save], sender=Category)
def delete_categories_cache(sender, instance, **kwargs):
    catalog_logger.info(f"Набор каталогов изменен. ID: {instance.id}")
    cache.delete("categories:list")
    cache.delete(f"categories:detail:{instance.slug}")
    if instance.parent is not None:
        cache.delete(f"categories:detail:{instance.parent.slug}")


@receiver([post_delete, post_save], sender=Product)
def delete_products_cache(sender, instance, **kwargs):
    catalog_logger.info(f"Набор товаров изменен. ID: {instance.id}")
    cache.delete_pattern("products:list:*")
    cache.delete(f"products:detail:{instance.slug}")