from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import GiftSerializer
from .models import Gift

class GiftCreateView(APIView):
    authentication_classes = [JWTAuthentication]  # Добавляем поддержку JWT
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GiftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

