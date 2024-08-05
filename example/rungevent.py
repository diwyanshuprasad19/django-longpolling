#!/usr/bin/env python
from gevent import monkey; monkey.patch_all()
from gevent.pywsgi import WSGIServer
import sys
import os
import django
from django.core.wsgi import get_wsgi_application

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'example.settings')
django.setup()

# Create WSGI application
application = get_wsgi_application()

# Host and port configuration
host = 'localhost'
port = 80
if len(sys.argv) > 1:
    url = sys.argv[1]
    if ':' in url:
        host, port = url.split(':')
    else:
        host = url

# Create and start WSGI server
server = WSGIServer((host, int(port)), application)
print(f"Starting server on http://{host}:{port}")
server.serve_forever()
