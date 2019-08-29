"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""
import os
import django
import environ
import sentry_sdk
import logging

from channels.routing import get_default_application

from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.aiohttp import AioHttpIntegration
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration

env = environ.Env()
SENTRY_DSN = env("SENTRY_DSN")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
SENTRY_LOG_LEVEL = env.int("DJANGO_SENTRY_LOG_LEVEL", logging.INFO)

django.setup()

sentry_logging = LoggingIntegration(
    level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
    event_level=logging.ERROR,  # Send no events from log messages
)

sentry_sdk.init(
    dsn=SENTRY_DSN,
    integrations=[sentry_logging, DjangoIntegration(), AioHttpIntegration()],
)

application = get_default_application()
application = SentryAsgiMiddleware(application)
