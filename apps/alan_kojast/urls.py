from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^guests/new/$', get_new_guest_token),
    url(r'^guests/waiting/$', set_guest_waiting_station),
    url(r'^vehicles/$', get_all_vehicles),
    url(r'^stations/$', get_all_stations),
    url(r'^access_points/$', get_all_access_points),
    # url(r'^vehicle/locate/$', ),
    url(r'^vehicle/status/$', set_vehicle_status),
    url(r'^stations/best$', get_most_populated_station),
]
