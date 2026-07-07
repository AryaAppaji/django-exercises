# Calling External APIs in Django using HTTPX

## What is an External API?

An external API (Application Programming Interface) is a service provided by another application or platform that allows your application to communicate with it and exchange data.

In simple terms, instead of building everything yourself, you can use services provided by third-party applications.

For example:

- Payment gateways
- Weather services
- SMS/OTP providers
- AI services
- Authentication providers
- Maps and location services

A real-world example:

When you make an online payment, your application usually communicates with a payment provider API to create and verify payments.

Similarly, when sending OTPs, applications communicate with SMS providers through APIs.

In Django, external APIs are commonly called to:

- Fetch data from another system
- Send data to another service
- Integrate third-party platforms
- Build real-time features

In this guide, we will learn how to call external APIs in Django using `httpx`.

## Why Use `httpx`?

`httpx` is a modern HTTP client library for Python that allows us to make API calls in a clean and simple way.

It supports:

- GET requests
- POST requests
- Headers
- Query parameters
- Timeouts
- Async support

For beginner-level Django projects, it provides a clean and easy syntax to work with external APIs.

Step-1: Install `httpx` using the following command:

```bash
uv add httpx
```

Or if you are using `pip`:

```bash
pip install httpx
```

Step-2: Create a Django app for working with external APIs.

Run the following command:

```bash
python manage.py startapp firstapp
```

After creating the app, register it inside `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    ...
    "firstapp",
]
```

Step-3: For better maintainability, store the external API base URL inside Django settings.

Open `settings.py` (or `base.py` if using split settings) and add:

```python
DUMMY_API_URL = "<your-api-server-url>"
```

This helps avoid hardcoding URLs repeatedly inside views.

Step-4: Now open `views.py` inside your app and define GET and POST API requests.

```python
import httpx
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view

api_base_url: str = settings.DUMMY_API_URL


@api_view(["GET"])
def get_data(request) -> JsonResponse:
    response = httpx.get(
        f"{api_base_url}/objects",
        timeout=10.0
    )

    return JsonResponse(response.json(), safe=False)


@api_view(["POST"])
def post_data(request) -> JsonResponse:
    response = httpx.post(
        f"{api_base_url}/objects",
        json=request.data,
        timeout=10.0
    )

    return JsonResponse(response.json(), safe=False)
```

### What is happening here?

#### GET Request

```python
response = httpx.get(f"{api_base_url}/objects")
```

This line sends a GET request to the external API and fetches data.

#### POST Request

```python
response = httpx.post(
    f"{api_base_url}/objects",
    json=request.data,
)
```

This line sends data to the external API.

`request.data` contains data sent from the request body.

#### Returning Response

```python
return JsonResponse(response.json(), safe=False)
```

This converts the external API response into JSON and returns it back from Django.

Step-5: Now register app URLs inside the project `urls.py`.

```python
from django.urls import include, path

urlpatterns = [
    path("get-data/", get_data),
    path("post-data/", post_data),
]
```

After this, your project structure may look like this:

```text
root_directory/
|--firstapp/
|  |--migrations/
|  |--__init__.py
|  |--admin.py
|  |--apps.py
|  |--models.py
|  |--tests.py
|  |--urls.py
|  |--views.py
|--project_folder/
|  |--settings.py
|  |--urls.py
|  |--wsgi.py
|  |--asgi.py
|--manage.py
|--pyproject.toml
|--README.md
|--uv.lock
```

Step-6: Run the server using:

```bash
uv run manage.py runserver
```

If the server starts successfully, your API integration is ready.

### GET Request

Open:

```text
http://127.0.0.1:8000/get-data/
```

This should return data fetched from the external API.

### POST Request

Call:

```text
http://127.0.0.1:8000/post-data/
```

with request body:

```json
{
  "name": "Apple MacBook Pro 16",
  "data": {
    "year": 2019,
    "price": 1849.99,
    "CPU model": "Intel Core i9",
    "Hard disk size": "1 TB"
  }
}
```

This will send data to the external API and return the response.

## Final Thoughts

You have now successfully learned how to:

- Install `httpx`
- Call external APIs in Django
- Create GET requests
- Create POST requests
- Configure URLs
- Test API responses

This is the foundation for integrating real-world services such as payment gateways, SMS providers, AI APIs, weather services, and authentication providers in Django applications.

The API server we have here is: [https://restful-api.dev/](https://restful-api.dev/)
