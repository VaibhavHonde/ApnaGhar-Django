from django.db import models
from django.contrib.auth.models import User

class Apt(models.Model):
    name = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties', null=True, blank=True)

    def __str__(self):
        return f"Name: {self.name} | Address: {self.address}"

class Amounts(models.Model):
    minimum = models.BigIntegerField()
    maximum = models.BigIntegerField()
    apt = models.ForeignKey(Apt, on_delete=models.CASCADE)

    def __str__(self):
        return f"Min: ${self.minimum} | Max: ${self.maximum}"

class Info(models.Model):
    phone_number = models.CharField(max_length=50)
    url = models.CharField(max_length=2083)
    apt = models.ForeignKey(Apt, on_delete=models.CASCADE)

    def __str__(self):
        return f"Phone Number:{self.phone_number} | URL:{self.url}"

class Coords(models.Model):
    long = models.FloatField()
    lat = models.FloatField()
    apt = models.ForeignKey(Apt, on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.long}, {self.lat})"

class Images(models.Model):
    src = models.CharField(max_length=2083)
    apt = models.ForeignKey(Apt, on_delete=models.CASCADE)

    def __str__(self):
        return f"Src: {self.src}"


class UserProfile(models.Model):
    USER_TYPES = [
        ('landlord', 'Landlord'),
        ('seller', 'Seller'),
        ('client', 'Client'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)
    contact_number = models.CharField(max_length=50, blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    properties_count = models.PositiveIntegerField(blank=True, null=True)
    budget = models.BigIntegerField(blank=True, null=True)
    move_in_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
    



