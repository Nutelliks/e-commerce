from django.db import models

DISCOUNT_TYPE = [
    ("FX", "fixed"),
    ("PR", "percent"),
]


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=2, choices=DISCOUNT_TYPE, default="FX")
    discount_value = models.DecimalField(max_digits=7, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    max_uses = models.PositiveIntegerField()
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    min_order_amount = models.PositiveIntegerField(null=True, blank=True)
    user = models.ManyToManyField("users.User", blank=True)
    once_per_user = models.BooleanField(default=False)

    class Meta:
        db_table = "promocodes"
        managed = True
        verbose_name = "PromoCode"
        verbose_name_plural = "PromoCodes"
