from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
User = get_user_model()

class Notification(models.Model):
    title = models.CharField(max_length=100)
    message = models.TextField()
    viewed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now, blank=True, null=True)

    @classmethod
    def get_unread_notifications(cls, user):
        return cls.objects.filter(user=user,viewed=False)
    
    class Meta:
        ordering = ['date']
   
    def __str__(self):
        return self.title

# def notif_save(sender, instance, **kwargs):
#     print('notif save')
# def notif_delete(sender, instance, **kwargs):
#     print("notif_delete")
# pre_save.connect(notif_save, sender=Notification)
# post_save.connect(notif_save, sender=Notification)
# post_delete.connect(notif_delete, sender=Notification)



class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete= models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.author.username
class Chat(models.Model):
    participants = models.ManyToManyField(User, blank=True)
    messages = models.ManyToManyField(Message, blank=True)
    room_name = models.TextField(blank=True)

    @classmethod
    def action(cls, room_name, action):
        if action == 'delete':
            cls.objects.get(room_name=room_name).delete()

    def __str__(self):
        return self.room_name


def last_20_messages(chat_name):
    chat = Chat.objects.get(room_name = chat_name)  
    return chat.messages.order_by('timestamp').all()[:20]


