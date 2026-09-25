from django.urls import path
from .views import (
    index,
    CategoryListCreateView,
    UnitListCreateView,
    ProductListCreateView,
    LoginView,
    LogoutView,
    ProfileView,
)

urlpatterns = [
    path("", index, name="master-index"),
    path(
        "categories/",
        CategoryListCreateView.as_view(),
        name="category-list",
    ),
    path("units/", UnitListCreateView.as_view(), name="unit-list"),
    path("products/", ProductListCreateView.as_view(), name="product-list"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
    path("auth/profile/", ProfileView.as_view(), name="profile"),
]
