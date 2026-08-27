from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import Category


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