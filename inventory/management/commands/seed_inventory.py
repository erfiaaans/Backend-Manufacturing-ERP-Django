from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from inventory.models import (
    Warehouse,
    InventoryStock,
    StockMovement,
)
from master.models import Product


class Command(BaseCommand):
    help = "Seed dummy data for inventory"

    @transaction.atomic
    def handle(self, *args, **options):
        User = get_user_model()
        user = User.objects.first()
        if not user:
            self.stdout.write(
                self.style.ERROR(
                    "User belum tersedia. Jalankan seed user terlebih dahulu."
                )
            )
            return
        warehouses_data = [
            {
                "code": "WH-001",
                "name": "Gudang Bahan Baku",
                "location": "Gedung A",
            },
            {
                "code": "WH-002",
                "name": "Gudang Barang Jadi",
                "location": "Gedung B",
            },
            {
                "code": "WH-003",
                "name": "Gudang Sparepart",
                "location": "Gedung C",
            },
        ]
        warehouses = {}
        for data in warehouses_data:
            warehouse, created = Warehouse.objects.get_or_create(
                code=data["code"],
                defaults={
                    "name": data["name"],
                    "location": data["location"],
                    "is_active": True,
                },
            )
            warehouses[data["code"]] = warehouse
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f"Warehouse created: {warehouse.code}")
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f"Warehouse created: {warehouse.code}")
                )

        products = list(Product.objects.all()[:5])
        if not products:
            self.stdout.write(
                self.style.ERROR(
                    "Product belum tersedia. Jalankan seed product terlebih dahulu."
                )
            )
            return
        stock_data = [
            ("WH-001", 0, 500, 50),
            ("WH-001", 1, 250, 25),
            ("WH-001", 2, 100, 20),
            ("WH-002", 0, 75, 10),
            ("WH-002", 1, 50, 10),
        ]
        for warehouse_code, product_index, quantity, minimum_stock in stock_data:
            if product_index >= len(products):
                continue
            product = products[product_index]
            warehouse = warehouses[warehouse_code]
            stock, created = InventoryStock.objects.get_or_create(
                product=product,
                warehouse=warehouse,
                defaults={
                    "quantity": quantity,
                    "reserved_quantity": 0,
                    "minimum_stock": minimum_stock,
                },
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Stock created: "
                        f"{product.name} - {warehouse_code} = {quantity}"
                    )
                )
        movement_data = [
            {
                "product_index": 0,
                "warehouse": "WH-001",
                "movement_type": StockMovement.MovementType.IN,
                "quantity": 500,
                "reference_type": "PURCHASE",
                "reference_id": 1,
                "notes": "Penerimaan bahan baku awal",
            },
            {
                "product_index": 0,
                "warehouse": "WH-001",
                "movement_type": StockMovement.MovementType.OUT,
                "quantity": 50,
                "reference_type": "PRODUCTION",
                "reference_id": 1,
                "notes": "Pengeluaran bahan baku untuk produksi",
            },
            {
                "product_index": 1,
                "warehouse": "WH-001",
                "movement_type": StockMovement.MovementType.IN,
                "quantity": 250,
                "reference_type": "PURCHASE",
                "reference_id": 2,
                "notes": "Penerimaan bahan baku",
            },
            {
                "product_index": 2,
                "warehouse": "WH-001",
                "movement_type": StockMovement.MovementType.ADJUSTMENT,
                "quantity": 100,
                "reference_type": "STOCK_OPNAME",
                "reference_id": 1,
                "notes": "Penyesuaian hasil stock opname",
            },
            {
                "product_index": 0,
                "warehouse": "WH-002",
                "movement_type": StockMovement.MovementType.IN,
                "quantity": 75,
                "reference_type": "PRODUCTION",
                "reference_id": 1,
                "notes": "Hasil produksi masuk gudang barang jadi",
            },
        ]
        for data in movement_data:
            if data["product_index"] >= len(products):
                continue
            product = products[data["product_index"]]
            warehouse = warehouses[data["warehouse"]]

            exists = StockMovement.objects.filter(
                product=product,
                warehouse=warehouse,
                movement_type=data["movement_type"],
                quantity=data["quantity"],
                reference_type=data["reference_type"],
                reference_id=data["reference_id"],
            ).exists()

            if not exists:
                StockMovement.objects.create(
                    product=product,
                    warehouse=warehouse,
                    movement_type=data["movement_type"],
                    quantity=data["quantity"],
                    reference_type=data["reference_type"],
                    reference_id=data["reference_id"],
                    notes=data["notes"],
                    created_by=user,
                )
        self.stdout.write(self.style.SUCCESS("\nInventory dummy data berhasil dibuat."))
