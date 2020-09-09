import asyncio
import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Chat, last_20_messages
from django.contrib.auth import get_user_model
User = get_user_model()

class ChatNotification(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['user']
        self.group_room_name = str(self.room_name) +'_group'
        async_to_sync(self.channel_layer.group_add)(
            self.group_room_name,
            self.channel_name
        ) 
        self.accept()
        print('***CONNECTED***')

    def disconnect(self,code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_room_name,
            self.channel_name
        )
        print("DISCONNECTED CODE: ",code)

    def recieve(self, text_data):
        print(" MESSAGE RECEIVED")
        data = json.loads(text_data)
        message = data['message']
        async_to_sync(self.channel_layer.group_send)(
            self.group_room_name,{
                "type": 'send_message_to_frontend',
                "message": message
            }
        )
    def send_message_to_frontend(self,event):
        print("EVENT TRIGERED")
        message = event['message']
        self.send(text_data=json.dumps({
            'message': message
        }))

class ChatConsumer(WebsocketConsumer):
    
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        user = self.scope['user']
        self.room_group_name = 'chat_%s' % self.room_name
        if not Chat.objects.filter(room_name = self.room_name).exists():
            chat = Chat.objects.create(room_name = self.room_name)
            chat.save()
            chat.participants.add(user)
            chat.save()
        else:
            chat = Chat.objects.get(room_name = self.room_name)
            if user not in chat.participants.all():
                chat.participants.add(user)
                chat.save()
        async_to_sync(self.channel_layer.group_add) (
            self.room_group_name,
            self.channel_name
        ) 
        
        async_to_sync(self.accept()) 

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard) (
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    
    def fetch_messages(self, data):
        messages = last_20_messages(data['chatID'])
        content = {
            'messages': self.messages_to_json(messages)
        }
        return self.send_message(content)

    def new_message(self, data):
        author = data['from']
        author_user = User.objects.get(username=author)
        message = Message.objects.create(
            author = author_user,
            content = data['message']
            )
        chat = Chat.objects.get(room_name = self.room_name)
        chat.messages.add(message)
        chat.save()
        content = {
            'command': 'new_message',
            'message': self.message_to_json(message)
        }
        return self.send_chat_message(content)

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        return {
            'author': message.author.username,
            'content': message.content,
            'timestamp': str(message.timestamp)
        }
    
    def send_chat_message(self, message): 
        print('send chat message')
        async_to_sync(self.channel_layer.group_send) (
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message'] 
        self.send(text_data=json.dumps(message))
             
    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }