"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""

import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware

import os
import django
from channels.routing import get_default_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

django.setup()
application = get_default_application()
