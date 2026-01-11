import os
from channels.routing import ProtocolTypeRouter, URLRouter   #The main traffic director protocol router #decides if the request is HTTP or WebSocket.
from channels.auth import AuthMiddlewareStack   # (knows who's logged in)
from channels.security.websocket import AllowedHostsOriginValidator  #checks who's allowed to connect
from django.core.asgi import get_asgi_application
from games.routing import websocket_urlpatterns   #

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')   #Tells Django which settings file to use

django_asgi_app = get_asgi_application()  #Creates the regular HTTP application that handles normal web pages

application = ProtocolTypeRouter({ #: Creates the main application that routes all traffic
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator( #The Security Guard that checks allowed to connects to hosts websocket
        AuthMiddlewareStack(  #adds user info to connections
            URLRouter(  #
                websocket_urlpatterns
            )
        )
    ),
})