from django.http import HttpResponseRedirect, JsonResponse
from .models import GuestTokens, Stations, Vehicles, AccessPoints
from .serializers import StationSerializer, VehicleSerializer, AccessPointSerializer
from .helpers import get_random_string
from django.views.decorators.http import require_http_methods
from datetime import datetime, timedelta
import pytz

utc = pytz.UTC


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

    time = 15

    if guest.waitingStation == station and guest.updated_at > (utc.localize(datetime.now()) - timedelta(minutes=30)):
        time = timedelta(minutes=time) - (utc.localize(datetime.now()) - guest.updated_at)
        time = time.seconds / 60
        if time < 0:
            time = 0
    else:
        guest.waitingStation = station
        guest.save()

    return JsonResponse({"status": 200, "result": {"time": time}})


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
    print(status)
    vehicle = Vehicles.objects.filter(accessKey=access_key).first()
    if vehicle is None:
        return JsonResponse({"status": 403})
    vehicle.active = True if status == '1' else False
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
    waiting_stations = GuestTokens.objects.filter(waitingStation__isnull=False).filter(
        updated_at__gt=time_threshold).all()

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


def locate_vehicle(request):
    if "key" in request.GET:
        access_key = request.GET['key']
    else:
        return JsonResponse({"status": 403})
    vehicle = Vehicles.objects.filter(access_key=access_key).first()
    if vehicle is None:
        return JsonResponse({"status": 403})
    ap = request.GET['ap']
    ap_list = ap.split('_')
    ap_map = {}
    addr_list = []
    for temp in ap_list:
        addr, strength = temp.split('-')
        ap_map[addr] = strength
        addr_list.append(addr)
    access_points = AccessPoints.objects.filter(unique_address__in=addr_list).all()

    lat_total, long_total, total_pwr = 0, 0, 0
    for access_point in access_points:
        temp_pwr = ap_map[access_point.unique_address]
        total_pwr += temp_pwr
        lat_total += temp_pwr * access_point.latitude
        long_total += temp_pwr * access_point.latitude

    final_lat, final_long = lat_total / total_pwr, long_total / total_pwr
    vehicle.latitude = final_lat
    vehicle.longitude = final_long
    vehicle.save()
    return JsonResponse({"status": 200})
