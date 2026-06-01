from django.shortcuts import render
import httpx
from rest_framework.decorators import api_view
from django.conf import settings
from django.http import JsonResponse

api_base_url: str = settings.DUMMY_API_URL

@api_view(["GET"])
def get_data(request) -> JsonResponse:
    response = httpx.get(f"{api_base_url}/objects")
    return JsonResponse(response.json(), safe=False)

@api_view(["POST"])
def post_data(request) -> JsonResponse:
    data: dict = {
  "name": "Apple MacBook Pro 16",
  "data": {
    "year": 2019,
    "price": 1849.99,
    "CPU model": "Intel Core i9",
    "Hard disk size": "1 TB"
  }
}
    response = httpx.post(f"{api_base_url}/objects", json=data)
    return JsonResponse(response.json(), safe=False)