import httpx
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework.decorators import api_view


api_base_url: str = settings.DUMMY_API_URL


@api_view(["GET"])
@extend_schema(
    summary="Retrieve objects",
    description=(
        "Retrieves a list of objects from the configured third-party API and returns the response to the client."
    ),
)
def get_data(request) -> JsonResponse:
    response = httpx.get(f"{api_base_url}/objects")
    return JsonResponse(response.json(), safe=False)


@api_view(["POST"])
@extend_schema(
    summary="Create an object",
    description=(
        "Creates a new object by sending the provided product information to the configured third-party API."
    ),
)
def post_data(request) -> JsonResponse:
    data: dict = {
        "name": "Apple MacBook Pro 16",
        "data": {
            "year": 2019,
            "price": 1849.99,
            "CPU model": "Intel Core i9",
            "Hard disk size": "1 TB",
        },
    }
    response = httpx.post(f"{api_base_url}/objects", json=data)
    return JsonResponse(response.json(), safe=False)


@api_view(["GET"])
@extend_schema(
    summary="Send a test email",
    description=(
        "Sends a test email to the email address provided through the "
        "`email` query parameter."
    ),
)
def send_email_to_user(request) -> JsonResponse:
    recipient_email = request.query_params.get("email")

    if not recipient_email:
        return JsonResponse(
            {"error": "The 'email' query parameter is required."},
            status=400,
        )

    subject = "Test Email"
    message = "This is a test email sent from Django."
    from_email = f"{settings.DEFAULT_FROM_EMAIL}"
    recipient_list = [recipient_email]

    try:
        send_mail(subject, message, from_email, recipient_list)
        return JsonResponse({"message": "Email sent successfully."})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
