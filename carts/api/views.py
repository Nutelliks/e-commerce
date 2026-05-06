from rest_framework.generics import RetrieveAPIView
from .serializers import CartSerializer
from ..models import Cart
from ..utils import get_or_create_cart


class CartRetrieveView(RetrieveAPIView):
    queryset = Cart.objects.all().prefetch_related("cart_items")
    serializer_class = CartSerializer


    def get_object(self):
        cart = get_or_create_cart(self.request)
        return cart