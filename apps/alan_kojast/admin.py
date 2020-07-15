from django.contrib import admin
from .models import GuestTokens, Stations, Vehicles, AccessPoints


class GuestTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'get_station', 'created_at', 'updated_at')

    def get_station(self, obj):
        ws = obj.waitingStation
        if ws is None:
            return ""
        else:
            return ws.name + "-" + str(ws.id)


class StationsAdmin(admin.ModelAdmin):
    list_display = ('gender', 'name', 'active', 'region', 'latitude', 'longitude', 'created_at', 'updated_at')


class VehiclesAdmin(admin.ModelAdmin):
    list_display = (
    'type', 'gender', 'full_capacity', 'number', 'active', 'latitude', 'longitude', 'get_station', 'created_at',
    'updated_at', 'accessKey')

    def get_station(self, obj):
        ws = obj.currentStation
        if ws is None:
            return ""
        else:
            return ws.name + "-" + str(ws.id)


class AccessPointsAdmin(admin.ModelAdmin):
    list_display = ('unique_address', 'latitude', 'longitude', 'created_at', 'updated_at')


admin.site.register(GuestTokens, GuestTokenAdmin)
admin.site.register(Stations, StationsAdmin)
admin.site.register(AccessPoints, AccessPointsAdmin)
