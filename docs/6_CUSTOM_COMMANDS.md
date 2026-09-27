# Custom Management Commands in Django

> [!NOTE]
> **Prerequisites:**
>
> 1. This guide assumes you have already configured environment variables using `django-environ` and configured a custom user model. If you haven't, complete the **[Configuring Environment Variables in Django](/docs/1_ENVIRONMENT_VARIABLES_SETUP.md)** and **[Creating a Custom User Model](/docs/5_CREATING_CUSTOM_USER_MODEL.md)** exercises before continuing.
> 2. **Database & Migrations Setup:** Django requires a configured database and applied migrations (such as user models and the `django_session` table) before executing commands that interact with the database. In this project, database configurations are loaded dynamically via environment variables using PostgreSQL.
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

## What is a Django Management Command?

Django management commands are CLI (Command Line Interface) scripts executed through `manage.py`, such as:
- `python manage.py runserver`
- `python manage.py migrate`
- `python manage.py createsuperuser`

Django provides a built-in framework that allows you to write your own custom management commands.

### Common Use Cases

- **Seeding Test / Demo Data:** Populating databases with sample records for local development or testing.
- **Automated / Scheduled Jobs:** Running cron jobs or batch tasks such as data cleanups, generating daily reports, or sending batch notification emails.
- **Data Imports / Exports:** Migrating data from external files (CSV, JSON) into database models without needing a web interface.
- **System Maintenance:** Resetting specific state or syncing caches.

---

## Directory Structure Convention

Django discovers management commands automatically using a specific directory layout inside any app listed in `INSTALLED_APPS`:

```text
app_name/
└── management/
    └── commands/
        └── your_command_name.py
```

- The file name directly determines the command name executed via `manage.py`.
- For example, creating `create_demo_users.py` inside `coreapp/management/commands/` registers the command:
  ```bash
  python manage.py create_demo_users
  ```
- The parent app (`coreapp`) must be present in `INSTALLED_APPS` inside `settings/base.py`.

---

## Step-1: Create the Management Package Directory Structure

Inside your app directory (here `coreapp`), create the required folder structure:

```bash
mkdir -p coreapp/management/commands
```

> [!TIP]
> You can also include empty `__init__.py` files inside both `management/` and `commands/` directories to ensure standard Python package recognition.

---

## Step-2: Create the Custom Command File

Create a file named `create_demo_users.py` inside `coreapp/management/commands/`:

```python
from django.core.management.base import BaseCommand
from ...models import CustomUser


class Command(BaseCommand):
    help: str = "Creates Demo Users"

    def handle(self, *args, **kwargs):
        demo_users: list[dict[str, str]] = [
            # User 1.
            {
                "username": "User 1",
                "email": "user1@example.com",
                "password": "User1@123",
                "phone_number": "9876543210",
                "country": "India",
            },
            # User 2.
            {
                "username": "User 2",
                "email": "user2@example.com",
                "password": "User2@123",
                "phone_number": "9876543211",
                "country": "India",
            },
            # User 3.
            {
                "username": "User 3",
                "email": "user3@example.com",
                "password": "User3@123",
                "phone_number": "9876543212",
                "country": "India",
            },
        ]

        for user in demo_users:
            if not CustomUser.objects.filter(email=user["email"]).exists():
                CustomUser.objects.create_user(**user)

        self.stdout.write(self.style.SUCCESS("Demo Users created successfully."))
```

---

## Step-3: What is Happening Here?

### 1. Subclassing `BaseCommand`

```python
from django.core.management.base import BaseCommand

class Command(BaseCommand):
```

Every custom command must define a class named `Command` that inherits from `BaseCommand`.

### 2. Help Text

```python
help: str = "Creates Demo Users"
```

This text is displayed when someone checks the command documentation using:

```bash
python manage.py create_demo_users --help
```

### 3. The `handle()` Method

```python
def handle(self, *args, **kwargs):
```

The `handle()` method is the main entry point where your command's execution logic lives. When you run `python manage.py create_demo_users`, Django calls this method.

### 4. Secure Password Hashing with `create_user()`

```python
CustomUser.objects.create_user(**user)
```

Instead of using `.create()`, we call `create_user()`. This ensures passwords are automatically hashed with Django's secure password hashing algorithms (e.g. PBKDF2 with SHA256) rather than stored as plain text.

### 5. Idempotent Data Seeding

```python
if not CustomUser.objects.filter(email=user["email"]).exists():
    CustomUser.objects.create_user(**user)
```

Before creating each user, the command checks whether a user with the given email already exists. This makes the command **idempotent**, meaning you can run it multiple times safely without causing duplicate user errors or crashes.

### 6. Colored Console Output

```python
self.stdout.write(self.style.SUCCESS("Demo Users created successfully."))
```

`self.stdout.write()` is used instead of standard `print()`. Combined with `self.style.SUCCESS()`, it formats the terminal output in green and automatically respects output redirection and `--no-color` flags.

---

## Step-4: Verify and Run the Command

### 1. Check Available Commands

Run:

```bash
python manage.py --help
```

You should see your command listed under the `[coreapp]` section:

```text
[coreapp]
    create_demo_users
```

### 2. Execute the Command

Run the custom management command:

```bash
python manage.py create_demo_users
```

Or using `uv`:

```bash
uv run manage.py create_demo_users
```

Output:

```text
Demo Users created successfully.
```

---

## Step-5: Verify Created Users

You can verify that the demo users were created:

### 1. In Django Admin

1. Start the server:
   ```bash
   uv run manage.py runserver
   ```
2. Navigate to `http://127.0.0.1:8000/admin/`.
3. Open **Custom users** under the **COREAPP** section to view the newly created users with their phone numbers and country details.

### 2. In Django Shell

Run:

```bash
python manage.py shell
```

Then query the database:

```python
from coreapp.models import CustomUser

for user in CustomUser.objects.all():
    print(user.username, user.email, user.phone_number, user.country)
```

---

## Project Structure

After adding custom management commands, your project structure will look like this:

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

## Final Thoughts

You have now successfully learned how to:

- Understand what Django management commands are and when to use them
- Follow Django's directory convention (`management/commands/`) for command auto-discovery
- Subclass `BaseCommand` and implement the `handle()` method
- Seed demo data safely and idempotently using `create_user()`
- Use `self.stdout.write` and `self.style.SUCCESS` for formatted CLI feedback
- Execute and verify custom commands via `manage.py`
