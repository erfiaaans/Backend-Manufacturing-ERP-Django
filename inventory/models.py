from django.db import models
from django.conf import settings
from master.models import Product


class Warehouse(models.Model):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "warehouses"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class InventoryStock(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="inventory_stocks"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="inventory_stocks"
    )
    quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    reserved_quantity = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    minimum_stock = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inventory_stocks"
        constraints = [
            models.UniqueConstraint(
                fields=["product", "warehouse"], name="unique_product_warehouse_stock"
            )
        ]

    def __str__(self):
        return f"{self.product} - {self.warehouse}"

    @property
    def available_quantity(Self):
        return self.quantity - self.reserved_quantity


class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        IN = "IN", "Stock In"
        OUT = "OUT", "Stock Out"
        ADJUSTMENT = "ADJUSTMENT", "Adjustment"

    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="stock_movements"
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.PROTECT, related_name="stock_movements"
    )
    movement_type = models.CharField(max_length=20, choices=MovementType.choices)
    quantity = models.DecimalField(max_digits=15, decimal_places=2)
    reference_type = models.CharField(max_length=50, blank=True, null=True)
    reference_id = models.PositiveBigIntegerField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="stock_movements",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "stock_movements"
        ordering = ["-created_at"]

        def __str__(self):
            return f"{self.movement_type} - " f"{self.product} - " f"{self.quantity}"
