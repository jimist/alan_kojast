from django.conf.urls import url

from apps.vehicles.views import get_all_vehicles

urlpatterns = [
    url(r'^get/$', get_all_vehicles),
]
