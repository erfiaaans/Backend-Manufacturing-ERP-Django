from django.urls import path
from .views import index, CategoryListCreateView, UnitListCreateView

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
    )
]