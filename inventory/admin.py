from django.contrib import admin
from .models import Warehouse, InventoryStock, StockMovement


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "location",
        "is_active",
        "created_at",
    )
    search_fields = (
        "code",
        "name",
    )
    list_filter = ("is_active",)


@admin.register(InventoryStock)
class InventoryStockAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "warehouse",
        "quantity",
        "reserved_quantity",
        "minimum_stock",
        "updated_at",
    )
    search_fields = (
        "product__name",
        "warehouse__name",
    )
    list_filter = ("warehouse",)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "warehouse",
        "movement_type",
        "quantity",
        "created_by",
        "created_at",
    )
    search_fields = (
        "product__name",
        "warehouse__name",
        "notes",
    )
    list_filter = (
        "movement_type",
        "warehouse",
    )
