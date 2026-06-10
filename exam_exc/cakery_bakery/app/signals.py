from django.db.models.signals import pre_save,pre_delete
from .models import *
from django.dispatch import receiver
import random

@receiver(pre_delete, sender=Baker)
def baker_deletion(sender, instance, **kwargs):
    cakes = Cake.objects.filter(baker = instance)

    other_bakers = Baker.objects.exclude(id=instance.pk)

    for cake in cakes:
        baker = random.choice(other_bakers)
        cake.baker = baker
        cake.save()