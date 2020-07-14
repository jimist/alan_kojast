from django.conf.urls import url

from .views import get_all_vehicles, get_new_guest_token

urlpatterns = [
    url(r'^guests/new/$', get_new_guest_token),
    url(r'^vehicles/get/$', get_all_vehicles),
]
