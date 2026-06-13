from django.db.models.signals import pre_save, pre_delete, post_save, post_delete
from django.dispatch import receiver

from .models import *

@receiver(pre_save, sender=Property)
def save_property(sender, instance, **kwargs):
    old_instance = Property.objects.filter(id=instance.id).first()
    if old_instance and old_instance.sold is False and instance.sold is True:
        property_agents = PropertyAgent.objects.filter(property=instance)
        for pa in property_agents:
            agent = pa.agent
            agent.completed_sales += 1
            agent.save()

@receiver([post_save, post_delete], sender=PropertyFeature)
def update_feature(sender, instance, **kwargs):
    property_feature = sender.objects.filter(property=instance.property)

    if property_feature:
        prop = instance.property
        prop.feature = ', '.join(f.feature.name for f in property_feature)
        prop.save()
