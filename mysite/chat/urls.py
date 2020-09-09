from django.urls import path, re_path
from . import views

app_name = "chat"
urlpatterns = [
    path('action/', views.action, name="action"),
    path('sendChatNotifications/<str:room_name>/', views.sendChatNotifications, name= "sendChatNotifications"),
    path('<int:chat_id>/', views.chat, name="chat"),
    path('<str:room_name>/', views.chatRoom, name='chat-room'),
    
]