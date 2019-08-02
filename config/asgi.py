"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""
import os
import django
import environ
import sentry_sdk

from channels.routing import get_default_application

from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware


env = environ.Env()
SENTRY_DSN = env("SENTRY_DSN")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

django.setup()
sentry_sdk.init(
    dsn=SENTRY_DSN, integrations=[DjangoIntegration(), AioHttpIntegration()]
)

application = get_default_application()
application = SentryAsgiMiddleware(application)
