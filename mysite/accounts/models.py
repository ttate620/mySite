from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True)
   

    def __str__(self):
        return f'{self.user.username} Profile'

    @classmethod
    def get_random(cls, n):
        return cls.objects.order_by("?").all()[:n]

    @classmethod
    def edit_user_profile(cls, field, newInfo):
        fields = ['image', 'bio', 'location']
        if field in fields:
            cls.field = info
            cls.save()
        

class Friend(models.Model):
    friends = models.ManyToManyField(Profile, default = None, related_name='friends')
    my_pending_friends = models.ManyToManyField(Profile, default = None, related_name='my_pending_friends')
    pending_friends = models.ManyToManyField(Profile, default = None, related_name='pending_friends')
    current_user_profile = models.ForeignKey(Profile, related_name="owner", null=True, on_delete=models.CASCADE)

    
    #returns true if friendship exists or is successful, false otherwise
    @classmethod
    def make_friend(cls, current_user_profile, new_friend_profile):
        selfFriend, created = cls.objects.get_or_create(current_user_profile = current_user_profile)
        newFriend, created = cls.objects.get_or_create(current_user_profile = new_friend_profile)
        if selfFriend.is_friend(new_friend_profile):
            return True
        if selfFriend.is_pending(new_friend_profile):
            selfFriend.pending_friends.remove(new_friend_profile)
            newFriend.my_pending_friends.remove(current_user_profile)
            selfFriend.friends.add(new_friend_profile)
            newFriend.friends.add(current_user_profile)
            return True
        
        else:
            selfFriend.my_pending_friends.add(new_friend_profile)
            newFriend.pending_friends.add(current_user_profile)
            return False
        
    
    #return true on success, false otherwise
    @classmethod
    def remove_friend(cls, current_user_profile, remove_friend_profile):
        friend, created = cls.objects.get_or_create(current_user_profile = current_user_profile)
        removeFriend, created = cls.objects.get_or_create(current_user_profile = remove_friend_profile)
        # if friend.is_pending(remove_friend_profile):
        #     removeFriend.pending_friends.remove(current_user_profile)
        #     friend.pending_friends.remove(remove_friend_profile)
        #     return True
        if friend.is_friend(remove_friend_profile):
            removeFriend.friends.remove(current_user_profile)
            friend.friends.remove(remove_friend_profile)
            return True
        else:
            return False
        

    def is_pending(self, profile):
        if profile in self.pending_friends.all():
            return True
        else:
            return False
    def my_is_pending(self, profile):
        if profile in self.my_pending_friends.all():
            return True
        else:
            return False
    def is_friend(self, profile):
        if profile in self.friends.all():
            return True
        else:
            return False

    def status(self, profile):
        if self.is_friend(profile):
            return 'friends'
        elif self.is_pending(profile):
            return 'pending1'
        elif self.my_is_pending(profile):
            return 'pending2'
        else:
            return 'none'

    def friend_list(self):
        return list(self.friends.all())
    def request_sent(self):
        return list(self.my_pending_friends.all())
    def request_sent_to_me(self):
        return list(self.pending_friends.all())
    def friend_list_users(self):
        qs = []
        for friend in self.friends.all():
            qs.append(friend.user)
     
        return qs
    def __str__(self):
        return str(self.friends.all())
        
