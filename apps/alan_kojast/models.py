from django.db import models
from .helpers import get_random_string

GENDERS = (
    ("M", "Male"),
    ("F", "Female"),
)
VEHICLE_TYPES = (
    ("B", "Bus"),
    ("C", "Car"),
    ("V", "Van"),
)


class Stations(models.Model):
    gender = models.CharField(max_length=1, choices=GENDERS)
    name = models.CharField(max_length=127)
    number = models.IntegerField(default=0)
    active = models.BooleanField(default=True)
    region = models.CharField(max_length=63, default='ferdowsi')
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GuestTokens(models.Model):
    token = models.CharField(max_length=127)
    waitingStation = models.ForeignKey(Stations, on_delete=models.SET_NULL, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Vehicles(models.Model):
    type = models.CharField(max_length=1, choices=VEHICLE_TYPES)
    gender = models.CharField(max_length=1, choices=GENDERS)
    full_capacity = models.IntegerField()
    number = models.CharField(max_length=31, null=True, default=None)
    active = models.BooleanField(default=False)
    latitude = models.FloatField(null=True)
    longitude = models.FloatField(null=True)
    currentStation = models.ForeignKey(Stations, on_delete=models.SET_NULL, default=None, null=True)
    accessKey = models.CharField(max_length=128, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if len(self.accessKey) < 50:
            self.accessKey = get_random_string(128)
        super(Vehicles, self).save(*args, **kwargs)


class AccessPoints(models.Model):
    unique_address = models.CharField(max_length=256)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
