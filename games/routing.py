#Real-time updates only go to players in the same room
 #Each game room gets its own WebSocket connection

from django.urls import re_path  # handle the real-time communication /see where is should message go 
from . import consumers

websocket_urlpatterns = [  #Creates a list of WebSocket routes
    re_path(r'ws/game/(?P<room_id>\w+)/$', consumers.GameConsumer.as_asgi()),  #Make this consumer ready to handle WebSocket connections
]
