from django.db import models

from core.models import BaseModel


class Cart(BaseModel):
    user = models.OneToOneField(to="users.User", blank=True, null=True)
    session_key = models.CharField(max_length=40, unique=True, blank=True, null=True)

    class Meta:
        db_table = 'carts'
        managed = True
        verbose_name = 'Cart'
        verbose_name_plural = 'Carts'
