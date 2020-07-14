from django.conf.urls import url

from .views import get_all_vehicles, get_new_guest_token, set_guest_waiting_station, get_all_stations

urlpatterns = [
    url(r'^guests/new/$', get_new_guest_token),
    url(r'^guests/waiting/$', set_guest_waiting_station),
    url(r'^vehicles/$', get_all_vehicles),
    url(r'^stations/$', get_all_stations),
]
