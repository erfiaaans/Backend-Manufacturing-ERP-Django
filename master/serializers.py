from rest_framework import serializers
from .models import Category, Unit, Product

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
        model = ProductSerializer
        fields =[
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