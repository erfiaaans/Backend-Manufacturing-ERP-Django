from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Seed dummy users for Manufacturing ERP"

    def handle(self, *args, **options):

        users = [
            {
                "username": "admin",
                "email": "admin@manufacturing.local",
                "password": "Admin123!",
                "first_name": "Budi",
                "last_name": "Administrator",
                "is_staff": True,
                "is_superuser": True,
            },
            {
                "username": "warehouse01",
                "email": "warehouse01@manufacturing.local",
                "password": "Warehouse123!",
                "first_name": "Andi",
                "last_name": "Warehouse",
            },
            {
                "username": "production01",
                "email": "production01@manufacturing.local",
                "password": "Production123!",
                "first_name": "Siti",
                "last_name": "Production",
            },
            {
                "username": "sales01",
                "email": "sales01@manufacturing.local",
                "password": "Sales123!",
                "first_name": "Rina",
                "last_name": "Sales",
            },
        ]

        for data in users:
            username = data["username"]
            password = data.pop("password")

            user, created = User.objects.get_or_create(
                username=username,
                defaults=data,
            )

            if created:
                user.set_password(password)
                user.save()

                self.stdout.write(
                    self.style.SUCCESS(f"User {username} berhasil dibuat")
                )
            else:
                self.stdout.write(self.style.WARNING(f"User {username} sudah tersedia"))

        self.stdout.write(self.style.SUCCESS("Seeder users selesai!"))
