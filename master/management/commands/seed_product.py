from django.core.management.base import BaseCommand

from master.models import Category, Product, Unit


class Command(BaseCommand):
    help = "Seed dummy product data"

    def handle(self, *args, **options):
        raw_material = Category.objects.get(
            name="Raw Material"
        )

        finished_goods = Category.objects.get(
            name="Finished Goods"
        )

        packaging = Category.objects.get(
            name="Packaging"
        )

        kg = Unit.objects.get(code="KG")
        pcs = Unit.objects.get(code="PCS")
        box = Unit.objects.get(code="BOX")

        products = [
            {
                "name": "Steel Plate",
                "sku": "RM-001",
                "category": raw_material,
                "unit": kg,
                "description": "Bahan baku baja",
                "price": 15000,
                "stock": 1000,
            },
            {
                "name": "Aluminium Sheet",
                "sku": "RM-002",
                "category": raw_material,
                "unit": kg,
                "description": "Bahan baku aluminium",
                "price": 25000,
                "stock": 500,
            },
            {
                "name": "Product A",
                "sku": "FG-001",
                "category": finished_goods,
                "unit": pcs,
                "description": "Produk jadi A",
                "price": 150000,
                "stock": 100,
            },
            {
                "name": "Product B",
                "sku": "FG-002",
                "category": finished_goods,
                "unit": pcs,
                "description": "Produk jadi B",
                "price": 200000,
                "stock": 75,
            },
            {
                "name": "Cardboard Box",
                "sku": "PKG-001",
                "category": packaging,
                "unit": box,
                "description": "Kemasan produk",
                "price": 5000,
                "stock": 300,
            },
        ]

        created_count = 0

        for data in products:
            product, created = Product.objects.get_or_create(
                sku=data["sku"],
                defaults=data,
            )

            if created:
                created_count += 1

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {product.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Already exists: {product.name}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSeeding completed. "
                f"{created_count} product created."
            )
        )