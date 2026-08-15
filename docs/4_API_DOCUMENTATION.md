# API Documentation in Django using drf-spectacular

> [!NOTE]
> **Prerequisites:**
>
> 1. This guide assumes you have already configured environment variables using `django-environ` and set up API endpoints. If you haven't, complete the **[Configuring Environment Variables in Django](/docs/1_ENVIRONMENT_VARIABLES_SETUP.md)** exercise before continuing.
> 2. **Database & Migrations Setup:** Django requires a configured database and system tables (such as the `django_session` table for session management) to generate and run API Docmentation. In this project, database configurations are loaded dynamically via environment variables using PostgreSQL.
>
> And to use postgres, run the following command:
>
> ```bash
> uv add psycopg
> ```
>
> if the above one is not working try `psycopg2` or `psycopg2-binary` try each one find out the
> compatible package for your system.
>
> First, make sure to add the database connection settings to your local `.env` file:
>
> ```env
> DB_ENGINE="django.db.backends.postgresql"
> DB_HOST="127.0.0.1"
> DB_PORT=5432
> DB_NAME="django_exercises"
> DB_USER="postgres"
> DB_PASSWORD="your_postgres_password"
> ```
>
> and change this "DATABASES" key in your settings file, we are replacing the default DB configuration as we have decided to use postgres you can use your own configuration based on the DB:
> DATABASES = {
>
> "default": {
> "ENGINE": env.str("DB_ENGINE"),
> "HOST": env.str("DB_HOST"),
> "PORT": env.int("DB_PORT"),
> "NAME": env.str("DB_NAME"),
> "USER": env.str("DB_USER"),
> "PASSWORD": env.str("DB_PASSWORD"),
> }
>
> }
>
> Then, apply the database migrations to create the necessary tables (including the `django_session` table):
>
> ```bash
> python manage.py migrate
> ```

## What is API Documentation?

API Documentation is a technical instruction manual that describes how to use and integrate with an API. It contains details about:

- API endpoints (URLs)
- Supported HTTP methods (GET, POST, etc.)
- Request parameters (query parameters, path variables)
- Request body structure (JSON payload structure)
- Response formats and status codes (e.g., 200 OK, 400 Bad Request, 500 Internal Server Error)
- Authentication and security methods required to call the API

OpenAPI (formerly Swagger Specification) is the industry-standard specification for describing RESTful APIs. Interactive tools like Swagger UI load this specification and provide a visual web interface where developers can explore and test endpoints directly from the browser.

## Why Use `drf-spectacular`?

`drf-spectacular` is a powerful OpenAPI 3.0 schema generation library for Django REST Framework (DRF).

It provides:

- **Automatic Schema Generation:** Inspects your DRF serializers, views, path variables, and query parameters to automatically construct an OpenAPI 3.0 schema.
- **Interactive UI Support:** Integrates out of the box with popular UI renderers like Swagger UI and Redoc.
- **Customization Hooks:** Allows you to customize specific endpoints using the `@extend_schema` decorator to describe summaries, parameters, custom response structures, and descriptions.
- **Static Schema Exporting:** Offers a management command to easily export your API schema to a YAML or JSON file (e.g., `schema.yml`).

Using `drf-spectacular` ensures that your API documentation is always up to date with your source code, avoiding the chore of maintaining documentation manually.

---

## Step-1: Install `drf-spectacular`

Install `drf-spectacular` using the below command.

```bash
uv add drf-spectacular
```

Or if you are using `pip`:

```bash
pip install drf-spectacular
```

---

## Step-2: Register and Configure in Settings

After installing register `drf_spectacular` inside `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    ...
    # External Package Apps.
    "rest_framework",
    "drf_spectacular",

    # Apps that are part of project.
    "firstapp",
]
```

Next, configure Django REST Framework to use `drf-spectacular` for generating API schemas, and define metadata details for your API documentation. Add the following settings at the bottom of the file:

```python
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "DJANGO EXERCISES",
    "DESCRIPTION": "This repository contains different examples implemented with django. Designed to help aspirants who want to step into django.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": True,
}
```

---

## Step-3: Set Up Documentation URLs

Configure the endpoints that serve both the raw schema file (YAML/JSON) and the interactive Swagger UI.

Open `project/urls.py` and modify it as follows:

```python
from django.contrib import admin
from django.urls import path
from firstapp import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path("admin/", admin.site.urls),
    # Exposes raw schema (YAML format by default)
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    # Exposes interactive Swagger UI loading the above schema
    path("api/docs", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
]
```

** Note: The schema endpoint is mandatory becuase without that the swagger UI won't render**

---

## Step-4: Document Your API Views

Use the `@extend_schema` decorator to document your API endpoints. It allows you to specify a summary, description, parameters, or response overrides.

Open `views.py` and decorate the view functions as shown below:

```python
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from django.http import JsonResponse
import httpx
from django.conf import settings
from django.core.mail import send_mail

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
```

---

## Step-5: Generate the Schema File

You can generate the API schema statically as a YAML file. This is useful for distributing the schema to frontend teams or keeping it in version control.

Run the following Django management command to generate/update the `schema.yml` file to generate whenever you have modified your Endpoints:

```bash
uv run manage.py spectacular --file schema.yml
```

This will create or update a file named `schema.yml` in your project's root directory containing the OpenAPI 3.0 representation of your API endpoints.

---

## Project Structure

After implementing the API documentation configurations, your project directory will look like this:

```text
root_directory/
|--firstapp/
|  |--views.py
|--project/
|  |--settings/
|  |  |--base.py
|  |--urls.py
|--manage.py
|--pyproject.toml
|--README.md
|--schema.yml
|--uv.lock
```

---

## Testing and Viewing the Documentation

### 1. Start the Development Server

```bash
uv run manage.py runserver
```

### 2. View Raw Schema (OpenAPI 3.0 Specs)

Open the following URL in your browser to see the generated YAML schema:

```text
http://127.0.0.1:8000/api/schema
```

### 3. Open the Interactive Swagger UI

Open the following URL in your browser to view the interactive documentation:

```text
http://127.0.0.1:8000/api/docs
```

From here, you can:

- View all endpoints (`/get-data/`, `/post-data/`, `/send-email/`, and the documentation schemas).
- Inspect endpoint methods, parameters, and description details generated from `@extend_schema`.
- Use the **"Try it out"** button to execute actual requests from the browser directly to your server and view real response bodies and headers.

---

## Final Thoughts

You have now successfully learned how to:

- Install and set up `drf-spectacular`
- Configure OpenAPI settings inside settings files
- Set up route handlers for the API schema and Swagger UI
- Document individual endpoints using `@extend_schema`
- Generate a static `schema.yml` configuration file
- Test and interact with your APIs using Swagger UI

API documentation is essential for web applications to ensure seamless collaboration between backend developers, frontend developers, mobile developers, and third-party integrations.
