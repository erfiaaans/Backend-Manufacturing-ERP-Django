from django.urls import path
from .views import index, CategoryListCreateView

urlpatterns = [
    path("", index, name="master-index"),
    path(
        "categories/",
        CategoryListCreateView.as_view(),
        name="category-list",
    ),
]