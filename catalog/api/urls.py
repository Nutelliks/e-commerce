from rest_framework import routers
from .views import CategoryViewSet, ProductViewSet


router = routers.SimpleRouter()
router.register(r"categories", CategoryViewSet)
router.register(r"products", ProductViewSet)