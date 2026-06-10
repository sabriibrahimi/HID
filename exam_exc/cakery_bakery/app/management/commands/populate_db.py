from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from app.models import Baker, Cake


class Command(BaseCommand):
    help = "Populate the cake shop with two bakers and demonstration cakes."

    def _baker(self, username, name, surname, phone, email):
        user, created = User.objects.get_or_create(username=username, defaults={"email": email})
        if created:
            user.set_password("test123")
            user.save()
        baker, _ = Baker.objects.get_or_create(
            user=user,
            defaults={
                "name": name,
                "surname": surname,
                "contact_phone": phone,
                "email": email,
            },
        )
        return baker

    def handle(self, *args, **options):
        kelly = self._baker("kelly_rowan", "Kelly", "Rowan", "070-111-111", "kelly@example.com")
        josiah = self._baker("josiah_barclay", "Josiah", "Barclay", "070-222-222", "josiah@example.com")
        cakes = [
            ("Chocolate Wonderland", 1200, 1.5, "Rich chocolate cake.", kelly),
            ("Berry Celebration", 1450, 1.8, "Fresh seasonal berry cake.", josiah),
            ("Vanilla Dream", 950, 1.2, "Classic vanilla cream cake.", kelly),
            ("Caramel Delight", 1100, 1.4, "Caramel cake with a soft center.", josiah),
        ]
        for name, price, weight, description, baker in cakes:
            Cake.objects.get_or_create(
                name=name,
                defaults={
                    "price": price,
                    "weight": weight,
                    "description": description,
                    "baker": baker,
                },
            )
        self.stdout.write(self.style.SUCCESS("Data successfully inserted."))
