# viewsets.py
import requests
from django.http import JsonResponse


def cocktail_list(request):
    res = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    return JsonResponse(res.json())


def create_user():
    pass
