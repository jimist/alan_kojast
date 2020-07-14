from django.conf.urls import url

from .views import get_all_vehicles

urlpatterns = [
    url(r'^get/$', get_all_vehicles),
]
