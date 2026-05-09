from rest_framework.routers import SimpleRouter
from .views import CartViewSet

router = SimpleRouter()

router.register('cart', CartViewSet, basename='cart')