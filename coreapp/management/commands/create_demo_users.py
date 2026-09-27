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
