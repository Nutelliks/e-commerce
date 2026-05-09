from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .serializers import CartSerializer, AddToCartSerializer, DeleteFromCartSerializer
from ..models import CartItem
from catalog.models import Product
from ..utils import get_or_create_cart


class CartViewSet(GenericViewSet):
    serializer_class = CartSerializer

    def get_object(self):
        cart = get_or_create_cart(self.request)
        return cart


    def list(self, request):
        cart = self.get_object()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    

    @action(detail=False, methods=["post"])
    def add(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data.get("product_id")
        quantity = serializer.validated_data.get("quantity")

        product = get_object_or_404(Product, id=product_id, is_active=True)
        cart = self.get_object()

        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product,
            defaults={"quantity": quantity, "price_snapshot": product.price}
        )

        if not created:
            item.quantity += quantity
            item.save()

        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    

    @action(detail=False, methods=["post"])
    def remove(self, request):
        serializer = DeleteFromCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data.get("product_id")
        quantity = serializer.validated_data.get("quantity")

        product = get_object_or_404(Product, id=product_id, is_active=True)
        cart = self.get_object()

        item = get_object_or_404(CartItem, cart=cart, product=product)

        if quantity:
            if quantity >= item.quantity:
                item.delete()
            else:
                item.quantity -= quantity
                item.save()
        else:
            item.delete()

        cart.refresh_from_db()
        serializer = self.get_serializer(cart)
        return Response(serializer.data)


# class CartRetrieveAPIView(RetrieveAPIView):
#     queryset = Cart.objects.all().prefetch_related("items")
#     serializer_class = CartSerializer

#     def get_object(self):
#         cart = get_or_create_cart(self.request)
#         return cart


# class CartAddAPIView(APIView):

#     def post(self, request):
#         serializer = AddToCartSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         product_id = serializer.validated_data.get("product_id")
#         quantity = serializer.validated_data.get("quantity")

#         product = get_object_or_404(Product, id=product_id, is_active=True)
#         cart = get_or_create_cart(request)

#         item, created = CartItem.objects.get_or_create(
#             cart=cart,
#             product=product,
#             defaults={"quantity": quantity, "price_snapshot": product.price}
#         )

#         if not created:
#             item.quantity += quantity
#             item.save()

#         cart_serializer = CartSerializer(cart)
#         return Response(cart_serializer.data)


# class CartRemoveAPIView(APIView):
    
    def post(self, request):
        serializer = DeleteFromCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data.get("product_id")
        quantity = serializer.validated_data.get("quantity")

        cart = get_or_create_cart(request)
        product = get_object_or_404(Product, id=product_id)
        item = get_object_or_404(CartItem, cart=cart, product=product)

        if quantity:
            item.quantity -= quantity
            if item.quantity <= 0:
                item.delete()
            else:
                item.save()
        else:
            item.delete()

        cart.refresh_from_db()

        serializer = CartSerializer(cart)
        return Response(serializer.data)