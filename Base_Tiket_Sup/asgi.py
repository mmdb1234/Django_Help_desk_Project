# Base_Tiket_Sup/asgi.py
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Base_Tiket_Sup.settings')

# Get Django ASGI application first
django_asgi_app = get_asgi_application()

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from chats.routing import websocket_urlpatterns

class WebSocketAuthMiddleware:
    """
    Middleware for WebSocket authentication
    """
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        # Add user to scope if authenticated
        scope['user'] = None
        
        # Get token from query string
        query_string = scope.get('query_string', b'').decode()
        from urllib.parse import parse_qs
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]
        
        if token:
            from rest_framework_simplejwt.tokens import AccessToken
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            try:
                access_token = AccessToken(token)
                user_id = access_token['user_id']
                user = await User.objects.aget(id=user_id)
                scope['user'] = user
            except Exception as e:
                print(f"WebSocket auth error: {e}")
        
        return await self.app(scope, receive, send)

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(
        WebSocketAuthMiddleware(
            URLRouter(websocket_urlpatterns)
        )
    ),
})