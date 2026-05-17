from django.utils import timezone


def validate_promocode(promocode, subtotal=None):

    errors = {}

    now = timezone.now()

    if not promocode.is_active:
        errors["is_active"] = "Промокод неактивен"

    if not (promocode.valid_from <= now <= promocode.valid_to):
        errors["valid_to"] = "Срок действия промокода истек"

    if (
        promocode.max_uses is not None
        and promocode.used_count >= promocode.max_uses
    ):
        errors["max_uses"] = "Лимит использований исчерпан"

    if (
        subtotal is not None
        and promocode.min_order_amount is not None
        and subtotal < promocode.min_order_amount
    ):
        errors["min_order_amount"] = (
            "Недостаточная сумма заказа"
        )


    if errors:
        return False, errors

    return True, "Промокод успешно валидирован"