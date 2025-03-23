from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Gift
from .serializers import GiftSerializer


class GiftListView(APIView):
    authentication_classes = [JWTAuthentication]  # Добавляем поддержку JWT
    permission_classes = [IsAuthenticated]

    def get(self, request):
        gifts = Gift.objects.filter(owner=request.user)
        serializer = GiftSerializer(gifts, many=True)
        return Response(serializer.data)


class GiftCreateView(APIView):
    authentication_classes = [JWTAuthentication]  # Добавляем поддержку JWT
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GiftSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GiftDetailView(APIView):
    authentication_classes = [JWTAuthentication]  # Добавляем поддержку JWT
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(Gift, pk=pk, owner=user)

    def get(self, request, pk):
        gift = self.get_object(pk, request.user)
        serializer = GiftSerializer(gift)
        return Response(serializer.data)

    def put(self, request, pk):
        gift = self.get_object(pk, request.user)
        serializer = GiftSerializer(gift, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        gift = self.get_object(pk, request.user)
        gift.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
