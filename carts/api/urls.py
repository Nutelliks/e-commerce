from django.urls import path
from .views import CartRetrieveAPIView, CartAddAPIView, CartRemoveAPIView


routers = [
    path('cart/', CartRetrieveAPIView.as_view(), name="get_cart"),
    path('cart/add/', CartAddAPIView.as_view(), name="add_cart"),
    path('cart/remove/', CartRemoveAPIView.as_view(), name='remove_cart')
]