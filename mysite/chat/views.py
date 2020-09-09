from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Chat, Notification
from accounts.models import Friend, Profile
from django.db import models
from django.contrib.auth import get_user_model
import json 
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

User = get_user_model()

def chat(request, chat_id):
    chatee = None
    if User.objects.filter(pk=chat_id):
        chatee = User.objects.get(pk=chat_id)
    profile = Profile.objects.get(user = request.user)
    friend = Friend.objects.get(current_user_profile=profile)
    friends = friend.friend_list_users()
   
    context = {
        'chat_id' : chat_id,
        'chatee' : chatee,
        'friends':friends,
        'chats' : Chat.objects.filter(models.Q(participants=request.user)), 
        'notifications': Notification.get_unread_notifications(request.user),
       
    }
    
    return render(request,"chat-start.html", context)

@login_required
def chatRoom(request, room_name):
    
    return render(request, 'chat-room.html', {
        'room_name': room_name
    })

def sendChatNotifications(request, room_name):
    friends = request.POST['friends_in_chat']
    if Chat.objects.filter(room_name=room_name).exists():
        return JsonResponse({'error':'True','message':'unavailable'})
    else:
        for fr in friends:
            # send_to_username = friends.get(fr)
            # send_to_user = User.objects.get(username=send_to_username)
            # print('notif')
            # notification = Notification(title=room_name, message='new chat in '+ room_name, viewed=False, user=send_to_user)
            # notification.save()
            send_notification(fr, room_name)
        return JsonResponse({'success':'True','message': 'available'})

def action(request):
    room_name = request.POST['room_name']
    action = request.POST['action']
    Chat.action(room_name, action)
    return JsonResponse({'success':'True'})

def send_notification(user_name, room_name):
    user = User.objects.filter(username = user_name)
    if user.exists() :
        user = user.first()
        channel_layer = get_channel_layer()
        room_group_name = user.username + '_group'
        async_to_sync(channel_layer.group_send)(
            room_group_name,
            {
                'type': 'send_message_to_frontend',
                'message': room_name
            }
        )