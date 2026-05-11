from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from .serializers import UserRegisterSerializer
from ..tasks import send_welcome_email


class UserRegisterAPIView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        send_welcome_email.delay(user.id)


