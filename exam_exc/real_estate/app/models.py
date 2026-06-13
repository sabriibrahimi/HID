from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Property(models.Model):
    name = models.CharField(max_length=101)
    description = models.TextField()
    area = models.FloatField()
    date = models.DateField()
    image = models.ImageField(upload_to='properties/', blank=True, null=True)
    reserved = models.BooleanField(default=False)
    sold = models.BooleanField(default=False)
    feature = models.CharField(max_length=255,blank=True, default="")

    def __str__(self):
        return f"{self.name} - {self.area} - {self.description}"

class Agent(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    contact_phone = models.CharField(max_length=255)
    linked_in_profile = models.CharField(max_length=255)
    completed_sales = models.IntegerField(default=0)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} - {self.surname}"

class PropertyAgent(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.property}--{self.agent}"

class Feature(models.Model):
    name = models.CharField(max_length=255)
    value = models.FloatField()

    def __str__(self):
        return f"{self.name} - {self.value}"

class PropertyFeature(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.property}--{self.feature}"





