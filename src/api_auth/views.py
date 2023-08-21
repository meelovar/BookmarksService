from django.contrib import auth
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response

from api_auth.serializers import UserLoginSerializer, UserRegisterSerializer


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer


class LoginView(generics.CreateAPIView):
    serializer_class = UserLoginSerializer
    queryset = auth.get_user_model().objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        headers = self.get_success_headers(serializer.data)

        auth.login(request, user)

        return Response(None, status.HTTP_202_ACCEPTED, headers=headers)


class LogoutView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = None

    def get(self, request, *args, **kwargs):
        auth.logout(request)

        return Response(None, status.HTTP_200_OK)
