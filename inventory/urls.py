from django.urls import path
from .views import (
    WarehouseListCreateView,
    WarehouseDetailView,
    InventoryStockListView,
    InventoryStockDetailView,
    StockMovementListView,
    StockMovementDetailView,
)

urlpatterns = [
    path(
        "warehouses/", WarehouseListCreateView.as_view(), name="warehouse-list-create"
    ),
    path(
        "warehouses/<int:pk>/", WarehouseDetailView.as_view(), name="warehouse-detail"
    ),
    path("stocks/", InventoryStockListView.as_view(), name="stock-list"),
    path("stocks/<int:pk>/", InventoryStockDetailView.as_view(), name="stock-detail"),
    path("movements/", StockMovementListView.as_view(), name="movement-list"),
    path(
        "movements/<int:pk>/", StockMovementDetailView.as_view(), name="movement-detail"
    ),
]
