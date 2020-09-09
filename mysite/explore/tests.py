from django.test import TestCase
from django.contrib.auth.models import User
from explore.models import create_subForum
from explore.models import create_forum
from explore.models import create_post
from explore.models import SubForum
from explore.models import Forum
from explore.models import Post

# User.objects.all().delete()


# user1 = User.objects.create_user(username = 'tiff__1')
# user2 = User.objects.create_user(username = 'tiff__2')
# forum1 = create_forum(user1, 'Forum1_', 'Forum1 description')
# forum2 = create_forum(user2, 'Forum2_', 'Forum2 description')
def create_test_users():
    for i in range(0,2):
        user = User.objects.create_user(username = 'tiff_' + str(i))
        user.save()

def create_test_forum():
    qs = list(User.objects.all())
    k = 0
    for user in qs:
        for i in range(0,2):
            forum = create_forum(user, 'forum' + str(k) + 'from user '+ str(user.username), 'forum description')
            forum.save()
            k+=1

def create_test_subforum():
    qs = list(Forum.objects.all())
    k=0
    for forum in qs:
        for i in range(0,2):
            subforum = create_subForum(forum.creator, 'subforum' + str(k) + 'from user' + str(forum.creator.username), 'subforum description', forum)
            subforum.save()
            k+=1
def create_test_posts():
    qs = list(SubForum.objects.all())
    k=0
    for subforum in qs:
        for i in range(0,3):
            post = create_post(subforum.creator, 'post' +str(k)+ ' content', subforum)
            k+=1
# create_test_users()
create_test_forum()
# create_test_subforum()
# create_test_posts()
# user1 = User.objects.get(username = 'tiff__1')
# user2 = User.objects.get(username = 'tiff__2')
# forum1 = Forum.objects.get(title='Forum1_')
# forum2 = Forum.objects.get(title='Forum2_')
# subForum1 = create_subForum(user1, 'Topic1', 'Topic1 description', forum1) 
# subForum2 = create_subForum(user2, 'Topic2', 'Topic2 description', forum2) 
# post1 = create_post(user1, 'Post1 content', subForum1)
# post2 = create_post(user2, 'Post2 content', subForum2)
# # # edit_user_profile(user, bio, location, birth_date)

# print(Forum.objects.all())
# print(SubForum.objects.all())
# print(Post.objects.all())

# Category.objects.filter(title="test title").delete()
# print(Category.objects.all())
# print(Forum.objects.all())
# print(Topic.objects.all())
# print(Post.objects.all())
