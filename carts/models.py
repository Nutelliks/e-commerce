from django.db import models

from core.models import BaseModel


class Cart(BaseModel):
    user = models.OneToOneField(to="users.User", on_delete=models.SET_NULL, blank=True, null=True)
    session_key = models.CharField(max_length=40, unique=True, blank=True, null=True)

    class Meta:
        db_table = "carts"
        managed = True
        verbose_name = "Cart"
        verbose_name_plural = "Carts"


class CartItem(models.Model):
    cart = models.ForeignKey(
        to="carts.Cart", on_delete=models.CASCADE, related_name="cart_items"
    )
    product = models.ForeignKey(
        to="catalog.Product", on_delete=models.SET_NULL, null=True
    )
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name="Количество")
    price_snapshot = models.DecimalField(
        max_digits=7, decimal_places=2, verbose_name="Зафиксированная цена"
    )
