"""
ASGI entrypoint. Configures Django and then runs the application
defined in the ASGI_APPLICATION setting.
"""
import os
import django
import environ

import sentry_sdk
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from channels.routing import get_default_application


env = environ.Env()
SENTRY_DSN = env("SENTRY_DSN")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

django.setup()
sentry_sdk.init(dsn=SENTRY_DSN)

application = get_default_application()

# this is slightly infuriating, now if you have daphene serving both
# async and not, it only reports on the asgi ... so you'll need to
# parse out into a WSGI and an ASGI process to monitor
application = SentryAsgiMiddleware(application)

sentry_sdk.init(dsn=SENTRY_DSN)
