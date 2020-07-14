from django.http import HttpResponseRedirect, JsonResponse
from .models import GuestTokens, Stations, Vehicles
from .serializers import StationSerializer, VehicleSerializer
from .helpers import get_random_string
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST", "GET"])
def get_new_guest_token(request):
    guest = GuestTokens()
    guest.save()
    guest.token = str(guest.id) + get_random_string(100)
    guest.save()
    return JsonResponse({"status": 200, "result": {"token": guest.token}})


def get_all_stations(request):
    queryset = Stations.objects.all()
    serializer = StationSerializer(queryset, many=True)
    return JsonResponse({"status": 200, "result": serializer.data})


@require_http_methods(["POST", "GET"])
def set_guest_waiting_station(request):
    print(request.GET)
    station_id = request.GET['station_id']
    token = request.GET['token']
    station = Stations.objects.filter(id=station_id).first()
    if station is None:
        return JsonResponse({"status": 404, "result": {"msg": "Station not found!"}})
    guest = GuestTokens.objects.filter(token=token).first()
    if guest is None:
        return JsonResponse({"status": 404, "result": {"msg": "Guest not found!"}})
    guest.waitingStation = station
    guest.save()
    return JsonResponse({"status": 200, "result": {"msg": "success"}})


def get_all_vehicles(request):
    queryset = Vehicles.objects.all()
    serializer = VehicleSerializer(queryset, many=True)
    return JsonResponse({"status": 200, "result": serializer.data})
