from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    is_active = models.BooleanField()

    # def __str__(self):
    #     return self.name

class Manufacturer(models.Model):
    CHOICES = [
        ('small', 'SMALL'),
        ('medium', 'MEDIUM'),
        ('large', 'LARGE')
    ]
    name = models.CharField(max_length=100)
    date_of_incorporation = models.DateField()
    type = models.CharField(max_length=100, choices=CHOICES)

    # def __str__(self):
    #     return self.name

class Supplement(models.Model):
    name = models.CharField(max_length=100)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to="photos/")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    # def __str__(self):
    #     return self.name

