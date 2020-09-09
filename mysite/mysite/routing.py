from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url, re_path
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator

import chat.routing


application = ProtocolTypeRouter({
    'websocket':AuthMiddlewareStack(
                    URLRouter(
                        chat.routing.websocket_urlpatterns 
                                  
            )
        )
    
})
