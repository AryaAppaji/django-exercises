# Creating a Custom User Model in Django

> [!NOTE]
> **Prerequisites:**
>
> 1. This guide assumes you have already configured environment variables using `django-environ`. If you haven't, complete the **[Configuring Environment Variables in Django](/docs/1_ENVIRONMENT_VARIABLES_SETUP.md)** exercise before continuing.
> 2. **Database & Migrations Setup:** Django requires a configured database and system tables (such as the `django_session` table for session management) to manage users and run the application. In this project, database configurations are loaded dynamically via environment variables using PostgreSQL.
>
> To use PostgreSQL with Python, install `psycopg`:
>
> ```bash
> uv add psycopg
> ```
>
> _(If `psycopg` has compatibility issues with your system, try `psycopg2` or `psycopg2-binary`)_.
>
> Make sure your database connection settings are configured in your local `.env` file:
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
> And verify the `DATABASES` setting inside `project/settings/base.py`:
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

---

## What is a Custom User Model?

By default, Django comes with a built-in `User` model (`django.contrib.auth.models.User`) that includes basic authentication fields:

- `username`
- `first_name`
- `last_name`
- `email`
- `password`
- `is_staff`, `is_active`, `is_superuser`
- `last_login`, `date_joined`

However, real-world applications often require additional user profile information, such as:

- Phone numbers
- Country or address details
- Profile avatars
- Roles or department info

Instead of creating a separate profile model linked with a `OneToOneField`, Django allows you to substitute the built-in user model with a **Custom User Model**.

> [!IMPORTANT]
> **Start with a Custom User Model early!**
> The official Django documentation strongly recommends configuring a custom user model at the very beginning of a new project before running your first `migrate` command. Changing `AUTH_USER_MODEL` later after foreign keys and initial migration tables have been created is complex and often requires resetting migration histories.

---

## Approaches to Customizing Users in Django

Django provides two primary classes for creating custom user models:

1. **`AbstractUser` (Recommended when keeping default authentication fields):**
   Inherits all default fields and permissions (`username`, `email`, `password`, permissions, groups, etc.) while allowing you to add new custom fields directly. This is the simplest and most common approach.
2. **`AbstractBaseUser` (For fully customized authentication):**
   Provides only core authentication mechanisms (`password`, `last_login`). You must define all fields (such as using `email` as the primary identifier instead of `username`) and write a custom user manager.

In this guide, we use **`AbstractUser`** to extend the default user model with `phone_number` and `country` fields.

---

## Step-1: Create a Django App for the User Model

It is recommended to place user and core models inside a dedicated app (such as `coreapp` or `accounts`).

Create the app by running:

```bash
python manage.py startapp coreapp
```

---

## Step-2: Define `CustomUser` in `models.py`

Open `coreapp/models.py` and subclass `AbstractUser`:

```python
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
```

### What is happening here?

- `AbstractUser`: Imports Django's built-in user class containing all default user fields and authentication logic.
- `phone_number`: Adds a new optional character field for storing contact numbers.
- `country`: Adds a new optional character field for storing user country information.
- `blank=True, null=True`: Allows these fields to be optional both in form validation and in the database.

---

## Step-3: Register App & Configure `AUTH_USER_MODEL` in Settings

Open `project/settings/base.py` and perform two important updates:

### 1. Add `coreapp` to `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # External Package Apps.
    "rest_framework",
    "drf_spectacular",
    # Apps that are part of project.
    "coreapp",
    "firstapp",
]
```

### 2. Set `AUTH_USER_MODEL`

Add the following setting to specify that Django should use your custom model instead of the default `auth.User`:

```python
AUTH_USER_MODEL = "coreapp.CustomUser"
```

> [!WARNING]
> Ensure `AUTH_USER_MODEL` is configured using the `"app_name.ModelName"` format before running `python manage.py migrate`.

---

## Step-4: Register `CustomUser` in Django Admin

To manage users in the Django Admin interface, register the model.

Open `coreapp/admin.py`:

```python
from django.contrib import admin
from .models import CustomUser

# Register your models here.
admin.site.register(CustomUser)
```

_(Tip: You can also subclass `django.contrib.auth.admin.UserAdmin` to customize the fields and display panels in the admin dashboard)._

---

## Step-5: Create and Apply Migrations

Now generate the initial migration file for `coreapp` and apply migrations to the database:

### 1. Create migrations

```bash
python manage.py makemigrations coreapp
```

This generates `coreapp/migrations/0001_initial.py` containing the `CreateModel` operation for `CustomUser`.

### 2. Apply migrations

```bash
python manage.py migrate
```

This creates all necessary database tables, including `coreapp_customuser`, user permissions, groups, and the `django_session` table.

---

## Step-6: Create Superuser and Verify in Admin

### 1. Create a superuser

Run the createsuperuser management command:

```bash
python manage.py createsuperuser
```

Provide the username, email, and password when prompted.

### 2. Start the development server

```bash
uv run manage.py runserver
```

### 3. Log in to Django Admin

1. Open your browser and navigate to:
   ```text
   http://127.0.0.1:8000/admin/
   ```
2. Log in using your newly created superuser credentials.
3. You will see **Custom users** listed under the **COREAPP** section.
4. Click on a user or click **Add Custom User** to verify that `phone_number` and `country` are available.

---

## Project Structure

After completing this setup, your project structure will look like this:

```text
root_directory/
|--coreapp/
|  |--migrations/
|  |  |--0001_initial.py
|  |  |--__init__.py
|  |--__init__.py
|  |--admin.py
|  |--apps.py
|  |--models.py
|  |--tests.py
|  |--views.py
|--firstapp/
|--project/
|  |--settings/
|  |  |--base.py
|  |  |--local.py
|  |--urls.py
|--manage.py
|--pyproject.toml
|--README.md
|--uv.lock
```

---

## Best Practice: Referencing the User Model in Other Apps

When defining foreign keys or relationships to the user model in other models or serializers, **never** import `CustomUser` directly.

Instead, follow Django best practices:

### In `models.py`:

Use `settings.AUTH_USER_MODEL`:

```python
from django.conf import settings
from django.db import models


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
```

### In views, serializers, or signals:

Use `get_user_model()`:

```python
from django.contrib.auth import get_user_model

User = get_user_model()
```

This ensures your codebase remains decoupled, maintainable, and aligned with standard Django architecture.

---

## Final Thoughts

You have now successfully learned how to:

- Understand why a custom user model is necessary
- Extend Django's authentication system using `AbstractUser`
- Add custom fields (`phone_number`, `country`)
- Configure `AUTH_USER_MODEL` in project settings
- Register the custom model in Django Admin
- Create migrations and set up the custom user table in PostgreSQL
- Follow best practices for referencing the user model across apps
