# Generating QR Codes and Barcodes in Django

> [!NOTE]
> **Prerequisites:**
>
> 1. This guide assumes you have already configured environment variables using `django-environ` and set up API endpoints. If you haven't, complete the **[Configuring Environment Variables in Django](/docs/1_ENVIRONMENT_VARIABLES_SETUP.md)** and **[Calling External APIs](/docs/2_CALLING_EXTERNAL_APIS.md)** exercises before continuing.
> 2. **Database & Migrations Setup:** Django requires a configured database and applied migrations (such as user models and the `django_session` table) to run the application server properly. In this project, database configurations are loaded dynamically via environment variables using PostgreSQL.
>
> To use PostgreSQL with Python, install `psycopg`:
>
> ```bash
> uv add psycopg
> ```
>
> _(If `psycopg` has compatibility issues with your system, try `psycopg2` or `psycopg2-binary`)_.
>
> Ensure database connection settings are configured in your local `.env` file:
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
> Verify the `DATABASES` setting inside `project/settings/base.py`:
>
> ```python
> DATABASES = {
>     "default": {
>         "ENGINE": env.str("DB_ENGINE"),
>         "HOST": env.str("DB_HOST"),
>         "PORT": env.int("DB_PORT"),
>         "NAME": env.str("DB_NAME"),
>         "USER": env.str("DB_USER"),
>         "PASSWORD": env.str("DB_PASSWORD"),
>     }
> }
> ```
>
> And ensure all migrations are applied:
>
> ```bash
> python manage.py migrate
> ```

---

## What are Barcodes and QR Codes?

Barcodes and QR (Quick Response) codes are optical machine-readable representations of data:

- **Barcodes (1D):** Linear patterns of parallel lines and spacings (such as **Code 128**) commonly used in retail, inventory management, logistics, and package tracking.
- **QR Codes (2D):** Two-dimensional matrix barcodes capable of storing significantly more data (URLs, alphanumeric identifiers, contact cards, authentication tokens) and readable from any angle.

### Why Return Images as Base64?

In modern web and mobile applications, creating physical image files on the server's disk for every generated barcode or QR code is inefficient and requires periodic cleanup.

Instead, we generate the image in-memory using an `io.BytesIO` buffer, encode the binary bytes into a **Base64 string**, and return it directly within a JSON API response.

Benefits of Base64 responses:
- **No Disk I/O:** Images are rendered purely in-memory.
- **Easy Frontend Rendering:** Clients can directly embed Base64 strings in HTML images using Data URIs:
  ```html
  <img src="data:image/png;base64,<base64_string>" alt="QR Code" />
  ```
- **Lightweight & Stateless:** Ideal for REST APIs and microservice architectures.

---

## Step-1: Install Required Libraries

To generate barcodes, QR codes, and render them as PNG images, install `qrcode`, `python-barcode`, and `pillow`:

If you are using `uv`:

```bash
uv add qrcode python-barcode pillow
```

Or if you are using `pip`:

```bash
pip install qrcode python-barcode pillow
```

- **`qrcode`**: Generates QR code matrix data.
- **`python-barcode`**: Generates linear 1D barcodes (such as Code 128, EAN, ISBN).
- **`pillow`**: The Python Imaging Library (PIL fork) used by both barcode and QR code libraries to draw and save image formats like PNG.

---

## Step-2: Implement Generation Views

Open `firstapp/views.py` and define the view functions for generating QR codes and barcodes:

```python
import base64
import io
import barcode
from barcode.writer import ImageWriter
from django.http import JsonResponse
import qrcode
from rest_framework.decorators import api_view


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
```

---

## Step-3: What is Happening Here?

### 1. In-Memory Image Buffer (`io.BytesIO()`)

```python
buffer = io.BytesIO()
```

`io.BytesIO` provides an in-memory binary stream. Instead of saving the generated image to a physical file on the server's disk, the image data is written directly to RAM.

### 2. QR Code Configuration & Generation

```python
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
```

- `version=1`: Controls the size of the QR Code matrix (1 to 40). `fit=True` automatically adjusts it to fit the data length.
- `error_correction`: Level of error correction (`ERROR_CORRECT_L` recovers up to ~7% of data).
- `box_size`: The number of pixels each box/grid square represents.
- `border`: The thickness of the margin (default is 4 boxes).
- `img.save(buffer, format="PNG")`: Renders the image as a PNG directly into the in-memory buffer.

### 3. Barcode Configuration & Generation

```python
barcode_obj = barcode.codex.Code128(data, writer=ImageWriter())
barcode_obj.write(buffer)
```

- `Code128`: A high-density 1D barcode format that supports alphanumeric characters.
- `ImageWriter()`: Tells `python-barcode` to output a bitmap image (PNG) using Pillow rather than a vector SVG.
- `barcode_obj.write(buffer)`: Writes the barcode PNG data directly into the buffer.

### 4. Base64 Encoding

```python
base64_image = base64.b64encode(buffer.getvalue()).decode("utf-8")
```

- `buffer.getvalue()`: Retrieves the raw binary PNG bytes from the in-memory stream.
- `base64.b64encode(...)`: Encodes binary bytes into Base64 ASCII bytes.
- `.decode("utf-8")`: Converts the bytes into a UTF-8 string so it can be serialized in a JSON response.

---

## Step-4: Register Endpoint URLs

Open `project/urls.py` and register the endpoints:

```python
from django.contrib import admin
from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from firstapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/docs", SpectacularSwaggerView.as_view(url_name="schema"), name="docs"),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path("get-data/", views.get_data, name="get_data"),
    path("post-data/", views.post_data, name="post_data"),
    path("send-email/", views.send_email_to_user, name="send_email_to_user"),
    # Barcode & QR Code endpoints
    path("generate-qrcode/", views.generate_qrcode, name="generate_qrcode"),
    path("generate-barcode/", views.generate_barcode, name="generate_barcode"),
]
```

---

## Step-5: Testing and Decoding the Generated Images

### 1. Start the Development Server

```bash
uv run manage.py runserver
```

### 2. Request QR Code

Open your browser or an API client (like Postman, curl, or Swagger UI):

```text
http://127.0.0.1:8000/generate-qrcode/
```

Response:

```json
{
  "qrcode": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

### 3. Request Barcode

```text
http://127.0.0.1:8000/generate-barcode/
```

Response:

```json
{
  "barcode": "iVBORw0KGgoAAAANSUhEUgAA..."
}
```

---

### 4. Decoding and Verifying the Base64 Image

To verify and view the generated image:

> [!TIP]
> Use the free online decoder tool **[Base64 Guru Image Decoder](https://base64.guru/converter/decode/image)** to test and inspect your output:
>
> 1. Open [https://base64.guru/converter/decode/image](https://base64.guru/converter/decode/image).
> 2. Copy the Base64 string value from the JSON response (`qrcode` or `barcode`).
> 3. Paste the string into the input box on the website.
> 4. Click **Decode Base64 to Image** to preview the rendered QR code or Barcode graphic!

You can also test the image directly in any web browser by opening the developer console or creating a quick HTML snippet:

```html
<img src="data:image/png;base64,<PASTE_BASE64_STRING_HERE>" alt="Generated Code" />
```

---

## Step-6: Update API Schema (Swagger)

Since `drf-spectacular` is configured, you can re-generate the static `schema.yml` file to include the new endpoints:

```bash
python manage.py spectacular --file schema.yml
```

Or view the endpoints interactively at `http://127.0.0.1:8000/api/docs`.

---

## Project Structure

After implementing barcode and QR code generation, your project structure looks like this:

```text
root_directory/
|--coreapp/
|  |--management/
|  |  |--commands/
|  |  |  |--create_demo_users.py
|  |--migrations/
|  |  |--0001_initial.py
|  |--admin.py
|  |--apps.py
|  |--models.py
|--firstapp/
|  |--migrations/
|  |--admin.py
|  |--apps.py
|  |--models.py
|  |--views.py
|--project/
|  |--settings/
|  |  |--base.py
|  |  |--local.py
|  |--urls.py
|--manage.py
|--pyproject.toml
|--README.md
|--schema.yml
|--uv.lock
```

---

## Final Thoughts

You have now successfully learned how to:

- Install and integrate `qrcode`, `python-barcode`, and `pillow` in a Django application
- Generate 2D QR codes and 1D Code 128 barcodes
- Use `io.BytesIO` to render images purely in-memory without saving temporary files to disk
- Convert binary image streams to Base64 strings for JSON API responses
- Test and decode Base64 images using [Base64 Guru](https://base64.guru/converter/decode/image) and Data URIs
