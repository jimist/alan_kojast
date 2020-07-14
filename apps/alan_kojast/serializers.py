from rest_framework import serializers
from .models import Stations, GENDERS, Vehicles, VEHICLE_TYPES


class StationSerializer(serializers.Serializer):
    gender = serializers.ChoiceField(choices=GENDERS)
    name = serializers.CharField(max_length=127)
    active = serializers.BooleanField(default=True)
    region = serializers.CharField(max_length=63)
    latitude = serializers.IntegerField()
    longitude = serializers.IntegerField()


class VehicleSerializer(serializers.Serializer):
    gender = serializers.ChoiceField(choices=GENDERS)
    type = serializers.ChoiceField(choices=VEHICLE_TYPES)
    full_capacity = serializers.IntegerField()
    number = serializers.CharField(max_length=31)
    active = serializers.BooleanField()
    latitude = serializers.IntegerField()
    longitude = serializers.IntegerField()
    currentStation = StationSerializer()
