from rest_framework import serializers
from .models import UserAddresses


class UserAddressSerializer(serializers.ModelSerializer):
    full_address = serializers.CharField(read_only=True, source="full_address")

    class Meta:
        model = UserAddresses
        fields = [
            "province",
            "city",
            "address",
            "building_number",
            "floor",
            "unit",
            "postal_code",
            "full_address",
        ]
