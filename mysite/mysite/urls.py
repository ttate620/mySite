from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    
    path('admin/', admin.site.urls),
    path('', include(('login.urls','login'), namespace='login')),
    path('account/', include(('accounts.urls','account'), namespace='account')),
    path('explore/', include(('explore.urls','explore'), namespace='explore')),
    path('chat/', include(('chat.urls','chat'), namespace='chat')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

