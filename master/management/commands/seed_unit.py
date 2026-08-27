from django.core.management.base import BaseCommand
from master.models import Unit
class Command(BaseCommand):
    help = "Seedd dummy unit data"
    def handle(self, *args, **options):
        units = [
            {"name": "Kilogram", "code": "KG"},
            {"name": "Gram", "code": "GR"},
            {"name": "Liter", "code": "LTR"},
            {"name": "Milliliter", "code": "ML"},
            {"name": "Piece", "code": "PCS"},
            {"name": "Box", "code": "BOX"},
            {"name": "Pack", "code": "PACK"},
        ]
        created_count = 0 
        for data in units:
            unit, created = Unit.objects.get_or_create(
                code=data["code"],
                defaults={
                    "name": data["name"],
                },
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(
                        f"Created: {unit.name}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"Already exist: {unit.name}"
                    )
                )
        self.stdout.write(
            self.style.SUCCESS(
                f"\nSeeding completed. {created_count} unit created."
            )
        )