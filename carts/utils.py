from .models import Cart


def get_cart(request):
    user = request.user
    session_key = request.session.session_key

    if user.is_authenticated:
        cart = Cart.objects.filter(user=user).first()

        return cart

    cart = Cart.objects.filter(session_key=session_key).first()

    return cart
