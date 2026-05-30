# Environment Variables Setup in Django

## What are Environment Variables?

Environment variables are values stored outside your application's source code that can be used to configure how an application behaves. Instead of hardcoding values directly in your project files, we store them separately and load them when the application runs.

For example, values like:

- Secret keys
- Database credentials
- API keys
- Debug mode
- Email configurations
- Third-party service credentials

are commonly stored using environment variables.

A simple example of an environment variable file (`.env`) looks like this:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_NAME=my_database
DATABASE_USER=my_user
DATABASE_PASSWORD=my_password
TIME_ZONE=Asia/Kolkata
```

## Why are Environment Variables Important?

Environment variables are important for several reasons:

### 1. Security

Sensitive information such as API keys, passwords, and secret keys should not be hardcoded inside the codebase because they may accidentally get pushed to version control systems like Git.

For example, this is **not recommended**:

```python
SECRET_KEY = "my-secret-key"
DATABASE_PASSWORD = "password123"
```

Instead, values should be loaded from environment variables.

### 2. Different Configurations for Different Environments

Applications usually run in multiple environments such as:

- Local development
- Testing
- Staging
- Production

Each environment may require different configurations.

For example:

- Local environment may use SQLite and `DEBUG=True`
- Production environment may use PostgreSQL and `DEBUG=False`

Using environment variables makes switching between environments easier without changing source code.

### 3. Cleaner and Maintainable Code

Keeping configuration outside the codebase makes the project easier to maintain and organize. Developers can update settings without modifying application logic.

### 4. Better Team Collaboration

When working in teams, each developer may have different local configurations (database credentials, local URLs, API keys, etc.). Environment variables allow everyone to use their own setup without modifying shared project files.

In this guide, we will use `django-environ` to load environment variables from a `.env` file and configure Django settings in a clean and scalable way. Let's get into the setup.

Step-1: Install `django-environ` using the following command

```bash
uv add django-environ
```

Step-2: Create a directory(folder) inside the project folder(`project` incase of this project).
Name it as `settings`.

Step-3: Create 2 files initially inside the `settings` directory you have created. So after that the directory structure should look like this:

```text
root_directory/
|--project_folder/
|  |--settings/
|  |  |--__init__.py
|  |  |--base.py
|  |--__init__.py
|  |--asgi.py
|  |--settings.py
|  |--urls.py
|  |--wsgi.py
|--.gitignore
|--.python-version
|--manage.py
|--pyproject.toml
|--README.md
|--uv.lock
```

Step-4: Now open `settings.py` and copy its contents
`settings/base.py`

Step-5: Now remove the `settings.py`

Step-6: Now inside `base.py` make the following changes. Change the following first few lines from this:

```python
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

```

to this:

```python

from pathlib import Path
import environ
env = environ.Env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent
environ.Env.read_env(BASE_DIR / '.env')
```

The reason we have added another `.parent` is we have moved the outer settings file to one more level deep additionally. And `import environ` is used to import the environ module and

```python
env = environ.Env()
```

is used to initialize `environ` module. And this line:

```python
environ.Env.read_env(BASE_DIR / '.env')
```

is used to load the path of .env file and link it to the application.

Step-7: Now open `asgi.py`, and change the following line, from this:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
```

to:

```python
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings.<your-settings-file>')
```

as because we have moved from a single settings file to a directory of settings files. And this file can be selected dynamically using a `.env` file with a varaible name `DJANGO_SETTINGS_MODULE`

Step-8: Repeat the same process as `Step-7` in both `wsgi.py` and `manage.py`.

Step-9: Now if you want to create another environment file do like this:

let's say `local.py` for local environment

```python
from .base import *

TIME_ZONE = env('TIME_ZONE', default='Asia/Kolkata')
```

Step-10: Now move all the sensitive data to the `.env` file like secret key, database credentials, API_KEYS etc,.

Step-11: Now run the server once and check everything is working fine.

Step-12: Do not commit `.env` file to your VCS(Version Control System Ex: GitHub) because it contains sensitive information. So for that create a `.gitignore` file if not present and `.env` in it.

Step-13: Since we are not committing the `.env` file to the VCS(Version Control System), we should create a `.env.example` file. This file provides an overview of all the required environment variables so that other team members can easily create and configure their local `.env` file.

**Example:**

```env
SECRET_KEY=
DEBUG=
DATABASE_NAME=
DATABASE_USER=
DATABASE_PASSWORD=
TIME_ZONE=
```

After all this the final setup will look like this:

```text
root_directory/
|--project_folder/
|  |--settings/
|  |  |--__init__.py
|  |  |--base.py
|  |  |--local.py
|  |--__init__.py
|  |--asgi.py
|  |--urls.py
|  |--wsgi.py
|--.env
|--.env.example
|--.gitignore
|--.python-version
|--manage.py
|--pyproject.toml
|--README.md
|--uv.lock
```
