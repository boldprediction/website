"""
WSGI config for webapp project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

if os.environ.get('dev_env',None) == "false":
    os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.test_settings'
else:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'webapp.settings')

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')

application = get_wsgi_application()
