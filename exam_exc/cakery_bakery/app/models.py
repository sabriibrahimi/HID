from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Baker(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=100)
    email = models.EmailField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.surname}"

class Cake(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    weight = models.FloatField()
    description = models.TextField()
    picture = models.ImageField(upload_to='cakes/', null=True, blank=True)
    baker = models.ForeignKey(Baker, on_delete=models.CASCADE, related_name='cakes')

    def __str__(self):
        return self.name

