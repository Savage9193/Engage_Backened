"""
WSGI config for engage_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "engage_backend.settings")

application = get_wsgi_application()
import os
if os.environ.get("CREATE_SUPERUSER_ON_STARTUP") == "1":
    from django.contrib.auth import get_user_model
    User = get_user_model()
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "test@example.com", "Test@1234")
import os
db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db.sqlite3')
if os.path.exists(db_path):
    os.remove(db_path)