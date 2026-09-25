from rest_framework import serializers
from .models import Category, Unit, Product
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(
        source="category.name",
        read_only=True,
    )
    unit_name = serializers.CharField(
        source="unit.name",
        read_only=True,
    )

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "sku",
            "category",
            "category_name",
            "unit",
            "unit_name",
            "description",
            "price",
            "stock",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError("Username atau password salah.")

        if not user.is_active:
            raise serializers.ValidationError("Akun pengguna tidak aktif.")

        attrs["user"] = user

        return attrs
