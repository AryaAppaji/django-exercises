import io
import base64
import httpx
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from drf_spectacular.utils import (
    extend_schema,
)
from rest_framework.decorators import api_view
import barcode
from barcode.writer import ImageWriter
import qrcode


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


@api_view(["GET"])
def generate_qrcode(request) -> JsonResponse:
    data: str = "ABC786"

    try:
        buffer = io.BytesIO()
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(buffer, format="PNG")
        base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return JsonResponse({"qrcode": base64_image})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@api_view(["GET"])
def generate_barcode(request) -> JsonResponse:
    data: str = "ABC786"

    try:
        buffer = io.BytesIO()
        barcode_obj = barcode.codex.Code128(data, writer=ImageWriter())
        barcode_obj.write(buffer)
        base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
        return JsonResponse({"barcode": base64_image})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
