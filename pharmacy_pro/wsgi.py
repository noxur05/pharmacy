"""
WSGI config for pharmacy_pro project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

# Add your project directory to the sys.path
path = '/home/noxur05/pharmacy'
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module
os.environ['DJANGO_SETTINGS_MODULE'] = 'pharmacy_pro.settings'

# Import Django's WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
