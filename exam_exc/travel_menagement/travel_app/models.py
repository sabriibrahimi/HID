from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class TourGuid(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"

class Trip(models.Model):

    place = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(default=0)
    duration = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to='visit/', null=True, blank=True)
    guide = models.ForeignKey(TourGuid, on_delete=models.CASCADE, related_name="guide_tour", null=True, blank=True)

    def __str__(self):
        return f"{self.place}"


