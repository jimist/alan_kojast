from django.http import HttpResponseRedirect, JsonResponse
from .models import GuestTokens, Stations, Vehicles, AccessPoints
from .serializers import StationSerializer, VehicleSerializer, AccessPointSerializer
from .helpers import get_random_string
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta


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


def get_all_access_points(request):
    queryset = AccessPoints.objects.all()
    serializer = AccessPointSerializer(queryset, many=True)
    return JsonResponse({"status": 200, "result": serializer.data})


def set_vehicle_status(request):
    if "key" in request.GET:
        access_key = request.GET['key']
    else:
        return JsonResponse({"status": 403})
    status = request.GET['status']
    vehicle = Vehicles.objects.filter(access_key=access_key).first()
    if vehicle is None or (status != 0 and status != 1):
        return JsonResponse({"status": 403})
    vehicle.active = True if status == 1 else False
    vehicle.save()
    return JsonResponse({"status": 200, "result": "success"})


def get_most_populated_station(request):
    if "key" in request.GET:
        access_key = request.GET['key']
    else:
        return JsonResponse({"status": 403})
    vehicle = Vehicles.objects.filter(access_key=access_key).first()
    if vehicle is None:
        return JsonResponse({"status": 403})

    time_threshold = datetime.now() - timedelta(minutes=30)
    waiting_stations = GuestTokens.objects.filter(waitingStation__isnull=False).filter(updated_at__gt=time_threshold).all()

    ws_map = {}
    for ws in waiting_stations:
        tmp_id = ws.waitingStation.id
        if tmp_id not in ws_map:
            ws_map[tmp_id] = 0
        ws_map[tmp_id] += 1
    most, top = 0, 0
    for sid, val in ws_map.items():
        if val > top:
            most = sid
    result = None
    if most > 0:
        station = Stations.objects.filter(id=sid).first()
        result = station.number

    return JsonResponse({"status": 200, "result": result})
