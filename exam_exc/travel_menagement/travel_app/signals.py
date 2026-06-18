import random

from django.db.models.signals import pre_delete
from django.dispatch import receiver

from .models import Trip, TourGuid


# When a tour guide is deleted, all of their
# destinations should be randomly reassigned to the remaining tour guides.
@receiver(pre_delete, sender=TourGuid)
def randomly(sender, instance, **kwargs):
    other_guides = TourGuid.objects.filter(id=instance.id)

    trips = Trip.objects.filter(guide=instance)

    for trip in trips:
        trip.guide = random.choice(other_guides)
        trip.save()
