from django.db import models


class Stations(models.Model):
    GENDERS = (
        ("M", "Male"),
        ("F", "Female"),
    )
    gender = models.CharField(max_length=1, choices=GENDERS)
    name = models.CharField(max_length=127)
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
