from rest_framework import serializers

from .models import Gift


class GiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gift
        fields = ["id", "name", "description", "url", "price", "is_reserved"]
        read_only_fields = ["id", "owner"]
