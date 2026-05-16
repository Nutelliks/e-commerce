from django.db import models
from django.core.exceptions import ValidationError

DISCOUNT_TYPE = [
    ("FX", "fixed"),
    ("PR", "percent"),
]


class PromoCode(models.Model):
    code = models.CharField(max_length=50, unique=True, db_index=True)
    discount_type = models.CharField(max_length=2, choices=DISCOUNT_TYPE, default="FX")
    discount_value = models.DecimalField(max_digits=7, decimal_places=2)
    valid_from = models.DateTimeField(db_index=True)
    valid_to = models.DateTimeField(db_index=True)
    max_uses = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    min_order_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    users = models.ManyToManyField("users.User", blank=True)
    once_per_user = models.BooleanField(default=False)


    class Meta:
        db_table = 'promocodes'
        verbose_name = 'PromoCode'
        verbose_name_plural = 'PromoCodes'

    def clean(self):
        errors = {}

        if self.valid_from >= self.valid_to:
            errors["valid_to"] = "Дата окончания должна быть позже даты начала"

        if self.discount_value <= 0:
            errors["discount_value"] = "Скидка должна быть больше 0"

        if self.discount_type == "PR" and self.discount_value > 100:
            errors["discount_value"] = "Процент скидки не может быть больше 100"

        if self.min_order_amount is not None and self.min_order_amount < 0:
            errors["min_order_amount"] = (
                "Минимальная сумма заказа не может быть отрицательной"
            )

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()

        super().save(*args, **kwargs)