# Sending Emails in Django using Gmail SMTP

> [!NOTE]
> **Prerequisite:** This guide assumes you have already configured environment variables using `django-environ`.
>
> If you haven't, complete the **[Configuring Environment Variables in Django using django-environ](/docs/1_ENVIRONMENT_VARIABLES_SETUP.md)** exercise before continuing.

## What is SMTP?

SMTP (Simple Mail Transfer Protocol) is the standard protocol used for sending emails over the internet.

Instead of building your own email server, your Django application can use an SMTP server provided by services like:

- Gmail
- Outlook
- Yahoo Mail
- Zoho Mail
- SendGrid
- Mailgun
- Amazon SES

In this guide, we will learn how to send emails in Django using Django's built-in `send_mail()` function with Gmail SMTP.

## Why use Django's built-in email functionality?

Django provides an email framework out of the box, so there is no need to install additional packages for basic email sending.

It provides features such as:

- Plain text emails
- HTML emails
- Multiple recipients
- Email attachments
- SMTP backend support
- Console backend for development

For beginner-level Django applications, `send_mail()` is the easiest way to start sending emails.

---

## Step-1: Enable Two-Factor Authentication (2FA)

Before using Gmail as your SMTP server, you must enable **Two-Factor Authentication (2FA)** on your Google account.

1. Open your Google Account.
2. Navigate to **Security**.
3. Enable **2-Step Verification** if it is not already enabled.

> Gmail does **not** allow applications to authenticate using your normal account password. Instead, you must generate an App Password.

---

## Step-2: Generate a Gmail App Password

After enabling Two-Factor Authentication:

1. Go to your Google Account.
2. Search for App Passwords in search bar.
3. Sign in again if prompted.
4. Enter a name such as:

```
Django Exercies
```

5. Click **Create**.

Google will generate a **16-character App Password** similar to:

```
abcd efgh ijkl mnop
```

Copy this password immediately because you won't be able to see that again. We will use it in Django settings.

> Never use your normal Gmail password inside your Django project.

---

## Step-3: Configure Email Settings

Open your `settings.py` (or `base.py` if using split settings) and add the following configuration.

```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587

if email port is 587 use,
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False

But if it is 465 use,
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True


EMAIL_HOST_USER = "your_email@gmail.com"
EMAIL_HOST_PASSWORD = "your_16_character_app_password_without_spaces"

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

Replace:

- `your_email@gmail.com` with your Gmail address.
- `your_16_character_app_password` with the App Password generated in the previous step. And remember one thing the generated password will contain spaces. But while mentioning in your `.env` remove the spaces.

> For production projects, it is recommended to store sensitive values such as email credentials in environment variables instead of hardcoding them.

---

## Step-4: Create a Django App

Create a new app for email functionality.

```bash
python manage.py startapp firstapp
```

Register the app inside `INSTALLED_APPS`.

```python
INSTALLED_APPS = [
    ...
    "firstapp",
]
```

---

## Step-5: Create the Email Sending View

Open `views.py` and add the following code.

```python
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework.decorators import api_view


@api_view(["GET"])
def send_email_to_user(request) -> JsonResponse:
    recipient_email = request.query_params.get("email")

    if not recipient_email:
        return JsonResponse(
            {"error": "The 'email' query parameter is required."},
            status=400,
        )

    subject = "Test Email"
    message = "This is a test email sent from Django."
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [recipient_email]

    try:
        send_mail(
            subject,
            message,
            from_email,
            recipient_list,
        )

        return JsonResponse(
            {"message": "Email sent successfully."}
        )

    except Exception as e:
        return JsonResponse(
            {"error": str(e)},
            status=500,
        )
```

---

## What is happening here?

### Getting the recipient email

```python
recipient_email = request.query_params.get("email")
```

This retrieves the recipient's email address from the query parameter.

Example:

```
http://127.0.0.1:8000/send-email/?email=user@example.com
```

---

### Creating the email

```python
subject = "Test Email"
message = "This is a test email sent from Django."
```

These define the subject and body of the email.

---

### Sender email

```python
from_email = settings.DEFAULT_FROM_EMAIL
```

This uses the sender email configured in `settings.py`.

---

### Recipient list

```python
recipient_list = [recipient_email]
```

`send_mail()` expects the recipients to be provided as a list.

---

### Sending the email

```python
send_mail(
    subject,
    message,
    from_email,
    recipient_list,
)
```

This sends the email using the configured SMTP server.

If everything is configured correctly, Gmail will deliver the email to the recipient.

---

## Step-6: Configure URLs

Then register your URLs inside the project `urls.py`.

```python
from django.urls import include, path
from firstapp.views import send_email_to_user

urlpatterns = [
    path("send-email/", send_email_to_user),
]
```

---

## Project Structure

After completing the setup, your project may look like this:

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

---

## Step-7: Run the Server

Start the development server.

```bash
uv run manage.py runserver
```

---

## Testing the API

Open the following URL in your browser:

```text
http://127.0.0.1:8000/send-email/?email=your_email@example.com
```

If everything is configured correctly, you should receive the email in your inbox.

Successful response:

```json
{
  "message": "Email sent successfully."
}
```

If the email query parameter is missing:

```json
{
  "error": "The 'email' query parameter is required."
}
```

---

## Final Thoughts

You have now successfully learned how to:

- Understand what SMTP is
- Configure Gmail SMTP in Django
- Generate a Gmail App Password
- Configure Django email settings
- Send emails using `send_mail()`
- Register the email API endpoint
- Test email sending

This is the foundation for implementing features such as account verification, password reset emails, OTP delivery, order confirmations, notifications, and other email-based workflows in Django applications.
