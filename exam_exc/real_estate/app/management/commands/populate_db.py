from datetime import date

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from app.models import Agent, Feature, Property, PropertyAgent, PropertyFeature


class Command(BaseCommand):
    help = "Populate the real estate agency with agents, features and demonstration properties."

    def _agent(self, username, name, surname, phone, linkedin, email):
        user, created = User.objects.get_or_create(username=username, defaults={"email": email})
        if created:
            user.set_password("test123")
            user.is_staff = True
            user.save()
        agent, _ = Agent.objects.get_or_create(
            user=user,
            defaults={
                "name": name,
                "surname": surname,
                "contact_phone": phone,
                "linked_in_profile": linkedin,
                "email": email,
            },
        )
        return agent

    def _feature(self, name, value):
        feature, _ = Feature.objects.get_or_create(name=name, defaults={"value": value})
        return feature

    def handle(self, *args, **options):
        ana = self._agent(
            "ana_stone",
            "Ana",
            "Stone",
            "+389-70-111-111",
            "https://linkedin.com/in/ana-stone",
            "ana.stone@example.com",
        )
        mark = self._agent(
            "mark_reed",
            "Mark",
            "Reed",
            "+389-70-222-222",
            "https://linkedin.com/in/mark-reed",
            "mark.reed@example.com",
        )

        elevator = self._feature("Elevator", 10000)
        pool = self._feature("Pool", 25000)
        garage = self._feature("Garage", 15000)
        garden = self._feature("Garden", 8000)

        listings = [
            ("Stone Residence", "Vodnanska quiet neighborhood", 180, "properties/house3.jpg", False, False, [elevator, garage], [ana]),
            ("Aero Villa", "Sunny hillside location", 230, "properties/aerocrete1.jpg", False, False, [pool, garden], [ana, mark]),
            ("Frame House", "Central residential zone", 95, "properties/frame1.jpg", False, False, [garage], [mark]),
            ("Reserved Family Home", "Near school and park", 145, "properties/house3.jpg", True, False, [garden], [ana]),
            ("Sold Lake House", "Lake view location", 210, "properties/frame1.jpg", False, True, [pool, garage], [mark]),
        ]

        for name, description, area, image, reserved, sold, features, agents in listings:
            prop, _ = Property.objects.get_or_create(
                name=name,
                defaults={
                    "description": description,
                    "area": area,
                    "date": date.today(),
                    "image": image,
                    "reserved": reserved,
                    "sold": sold,
                },
            )
            for agent in agents:
                PropertyAgent.objects.get_or_create(property=prop, agent=agent)
            for feature in features:
                PropertyFeature.objects.get_or_create(property=prop, feature=feature)

        self.stdout.write(self.style.SUCCESS("Data successfully inserted."))
