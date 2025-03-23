from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, RegisterSerializer, UserSerializer

# Create your views here.

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data

        refresh = RefreshToken.for_user(user)
        return Response(
            {"access": str(refresh.access_token), "refresh": str(refresh)},
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    authentication_classes = [JWTAuthentication]  # Добавляем поддержку JWT
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Добавляем токен в черный список
            return Response({"message": "logout"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(
                {"error": "error token"}, status=status.HTTP_400_BAD_REQUEST
            )


class ProfileView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]  # Добавляем поддержку JWT
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        user_data = {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username,
            "phone_number": (
                user.phone_number if hasattr(user, "phone_number") else None
            ),
        }
        return Response(user_data)


class UserUpdateView(APIView):
    authentication_classes = [JWTAuthentication]  # Добавляем поддержку JWT
    permission_classes = [IsAuthenticated]  # Только авторизованные пользователи

    def put(self, request):
        user = request.user  # Берем текущего пользователя
        serializer = UserSerializer(
            user, data=request.data, partial=True
        )  # Разрешаем частичное обновление

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
