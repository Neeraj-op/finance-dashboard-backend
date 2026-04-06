"""
WSGI config for finance backend project.
"""
import os
from django.core.wsgi import get_wsgi_application
from decouple import config

# Use production settings if not in debug mode
if not config('DEBUG', default=False, cast=bool):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.production_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()