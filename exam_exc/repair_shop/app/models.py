from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class Manufacturer(models.Model):
    name = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    owner = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Car(models.Model):
    car_type = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, models.CASCADE)
    max_speed = models.FloatField(null=True, blank=True)
    color = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.car_type}"

class Workshop(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField(null=True, blank=True)
    repair_old_times = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return self.name

class Repair(models.Model):
    code = models.CharField(max_length=225)
    date = models.DateField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='repairs/')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True, blank=True)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.code} - {self.date}"

class WorkshopManufacturer(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    workshop = models.ForeignKey(Workshop, on_delete=models.CASCADE)
