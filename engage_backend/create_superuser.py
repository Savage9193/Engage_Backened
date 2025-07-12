import os
from django.contrib.auth import get_user_model

User = get_user_model()

username = os.environ.get("DJANGO_ADMIN_USER", "admin")
email = os.environ.get("DJANGO_ADMIN_EMAIL", "admin@example.com")
password = os.environ.get("DJANGO_ADMIN_PASS", "admin123")

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print("✅ Superuser created")
else:
    print("ℹ️ Superuser already exists")
