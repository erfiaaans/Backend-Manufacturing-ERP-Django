from django.urls import path
from .views import index, CategoryListCreateView, UnitListCreateView, ProductListCreateView

urlpatterns = [
    path("", index, name="master-index"),
    path(
        "categories/",
        CategoryListCreateView.as_view(),
        name="category-list",
    ),
    path(
        "units/",
        UnitListCreateView.as_view(),
        name="unit-list"
    ),
    path(
        "products/",
        ProductListCreateView.as_view(),
        name="product-list"
    )
]