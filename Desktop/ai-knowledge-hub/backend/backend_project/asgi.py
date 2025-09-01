import os
from django.core.asgi import get_asgi_application
import socketio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')


# Django ASGI app
django_asgi_app = get_asgi_application()

# Try to import a Socket.IO server instance from apps.ai.llm_service
# If not available yet, create a fallback server so the ASGI app still mounts.
try:
    from apps.ai.llm_service import sio  # expected to be an AsyncServer instance
except Exception:
    sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')

# Mount Socket.IO on the Django ASGI application.
# Note: socketio_path can be customized; frontend ChatBox uses path '/ws/socket.io'
application = socketio.ASGIApp(sio, django_asgi_app, socketio_path="/ws/socket.io")
from apps.ai.llm_service import sio
application = socketio.ASGIApp(sio, django_asgi_app, socketio_path="/ws/socket.io")
