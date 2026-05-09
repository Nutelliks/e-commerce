from .models import Cart


def get_or_create_cart(request):
    user = request.user
    session_key = request.session.session_key

    anon_cart, _ = Cart.objects.get_or_create(
        session_key=session_key, user__isnull=True
    )

    if user.is_authenticated:
        user_cart, _ = Cart.objects.get_or_create(user=user)

        if anon_cart != user_cart:
            for item in anon_cart.items.all():
                existing = user_cart.items.filter(product=item.product).first()

                if existing:
                    existing.quantity += item.quantity
                    existing.save()
                else:
                    item.cart = user_cart
                    item.save()

            anon_cart.delete()

        return user_cart

    return anon_cart
