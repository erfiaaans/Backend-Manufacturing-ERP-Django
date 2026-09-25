from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .serializers import LoginSerializer

from .models import Category, Unit, Product


def index(request):
    return JsonResponse({"message": "Master API berhasil"})


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
                {"message": "Name wajib diisi"}, status=status.HTTP_400_BAD_REQUEST
            )

        category = Category.objects.create(name=name)

        return Response(
            {
                "id": category.id,
                "name": category.name,
            },
            status=status.HTTP_201_CREATED,
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
                {"message": "Name wajib diisi"},
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
                    "name": product.category.name,
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
            return Response(
                {"messsage": "name, category_id, dan unit_id wajib diisi"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response(
                {"message": "Category tidak ditemukan"},
                status=status.HTTP_404_NOT_FOUND,
            )
        try:
            unit = Unit.objects.get()(id=unit_id)
        except Unit.DoesNotExist:
            return Response(
                {"message": "Unit tidak ditemukan"},
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


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "Login berhasil.",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "is_staff": user.is_staff,
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"message": "Login gagal.", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "is_staff": user.is_staff,
                "is_superuser": user.is_superuser,
            }
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                {"message": "Refresh token wajib disertakan."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"message": "Logout berhasil."}, status=status.HTTP_200_OK)

        except TokenError:
            return Response(
                {
                    "message": "Refresh token tidak valid atau sudah tidak dapat digunakan."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
