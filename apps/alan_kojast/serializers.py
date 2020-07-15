from rest_framework import serializers
from .models import Stations, GENDERS, Vehicles, VEHICLE_TYPES


class StationSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    gender = serializers.ChoiceField(choices=GENDERS)
    name = serializers.CharField(max_length=127)
    number = serializers.IntegerField()
    active = serializers.BooleanField(default=True)
    region = serializers.CharField(max_length=63)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()


class VehicleSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    gender = serializers.ChoiceField(choices=GENDERS)
    type = serializers.ChoiceField(choices=VEHICLE_TYPES)
    full_capacity = serializers.IntegerField()
    number = serializers.CharField(max_length=31)
    active = serializers.BooleanField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    currentStation = StationSerializer()


class AccessPointSerializer(serializers.Serializer):
    unique_address = serializers.CharField(max_length=256)
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
