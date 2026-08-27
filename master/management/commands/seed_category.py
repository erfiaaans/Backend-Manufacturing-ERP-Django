from django.core.management.base import BaseCommand
from master.models import Category
class Command(BaseCommand):
    help = "Seed dummy category data"
    def handle(self, *args, **options):
        categories = [
            {
                "name": "Raw Material",
                "description": "Bahan baku untuk proses produksi",
            },
            {
                "name": "Finished Goods",
                "description": "Produk jadi hasil proses produksi",
            },
            {
                "name": "Semi Finished Goods",
                "description": "Produk setengah jadi",
            },
            {
                "name": "Packaging",
                "description": "Material untuk kebutuhan packaging",
            },
            {
                "name": "Spare Part",
                "description": "Suku cadang mesin dan peralatan",
            },
        ]
        created_count = 0
        for data in categories:
            category, created = Category.objects.get_or_create(
                name=data["name"],
                defaults={
                    "description": data["description"],
                },
            )
            if created:
                created_count +=1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {category.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {category.name}"
                    )
                )
        self.stdout.write(
            self.style.SUCCESS(
                f"\nSeeding completed. {created_count} category created."
            )
        )