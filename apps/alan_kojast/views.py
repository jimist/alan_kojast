from django.http import HttpResponseRedirect, JsonResponse
from .models import GuestTokens
from .helpers import get_random_string
import random
import string


def get_new_guest_token(request):
    guest = GuestTokens()
    guest.save()
    guest.token = str(guest.id) + get_random_string(100)
    guest.save()
    return JsonResponse({"status": 200, "info": {"token": guest.token, "waiting": guest.waiting}})


def get_all_vehicles(request):
    return JsonResponse({"status": 200, "message": "test"})
