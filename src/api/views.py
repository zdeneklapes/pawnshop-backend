# views.py
import requests
from django.http import JsonResponse

# In production, this should be set as an environment variable
API_KEY = 1


def cocktail_list(request):
    res = requests.get("https://jsonplaceholder.typicode.com/todos/1")
    return JsonResponse(res.json())
