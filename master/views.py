from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Category, Unit, Product


def index(request):
    return JsonResponse({
        "message": "Master API berhasil"
    })


class CategoryListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        categories = Category.objects.all()

        data = [
            {
                "id": category.id,
                "name": category.name,
            }
            for category in categories
        ]

        return Response(data)

    def post(self, request):
        name = request.data.get("name")

        if not name:
            return Response(
                {
                    "message": "Name wajib diisi"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        category = Category.objects.create(
            name=name
        )

        return Response(
            {
                "id": category.id,
                "name": category.name,
            },
            status=status.HTTP_201_CREATED
        )
        
class UnitListCreateView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        units = Unit.objects.all()

        data = [
            {
                "id": unit.id,
                "name": unit.name,
            }
            for unit in units
        ]

        return Response(data)

    def post(self, request):
        name = request.data.get("name")

        if not name:
            return Response(
                {
                    "message": "Name wajib diisi"
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        unit = Unit.objects.create(name=name)

        return Response(
            {
                "id": unit.id,
                "name": unit.name,
            },
            status=status.HTTP_201_CREATED,
        )
class ProductListCreateView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        products = Product.objects.select_related(
            "category",
            "unit",
        ).all()
        data = [
            {
                "id": product.id,
                "name": product.name,
                "category": {
                    "id": product.category.id,
                    "name":product.category.name,
                },
                "unit": {
                    "id": product.unit.id,
                    "name": product.unit.name,
                },
            }
            for product in products
        ]
        return Response(data)
    def post(self, request):
        name = request.data.get("name")
        category_id = request.data.get("category_id")
        unit_id = request.data.get("unit_id")
        
        if not name or not category_id or not unit_id:
            return Response({
                "messsage": "name, category_id, dan unit_id wajib diisi"
            },
            status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response(
                {
                    "message": "Category tidak ditemukan"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            unit = Unit.objects.get()(id=unit_id)
        except Unit.DoesNotExist:
            return Response(
                {
                    "message": "Unit tidak ditemukan"
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        product = Product.objects.create(
            name=name,
            category=category,
            unit=unit,
        )
        return Response(
            {
                "id": product.id,
                "name": product.name,
                "category": {
                    "id": product.category.id,
                    "name": product.category.name,
                },
                "unit": {
                    "id": product.unit.id,
                    "name": product.unit.name,
                },
            },
            status=status.HTTP_201_CREATED,
        )
            