from django.conf.urls import url

from .views import get_all_vehicles, get_new_guest_token, set_guest_waiting_station

urlpatterns = [
    url(r'^guests/new/$', get_new_guest_token),
    url(r'^guests/waiting/$', set_guest_waiting_station),
    url(r'^vehicles/get/$', get_all_vehicles),
]
