from django.db import models

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
    active = models.BooleanField(default=True)
    region = models.CharField(max_length=63, default='ferdowsi')
    latitude = models.IntegerField()
    longitude = models.IntegerField()
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
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    currentStation = models.ForeignKey(Stations, on_delete=models.SET_NULL, default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class AccessPoints(models.Model):
    unique_address = models.CharField(max_length=256)
    latitude = models.IntegerField()
    longitude = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
