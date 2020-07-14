from django.http import HttpResponseRedirect, JsonResponse


def get_all_vehicles(request):
    return JsonResponse({"status": 200, "message": "test"})
