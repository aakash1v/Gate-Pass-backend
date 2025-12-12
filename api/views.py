from django.http import JsonResponse


def home(req):
    return JsonResponse({"msg": "Backend server !!"})
