from django.db import models
from django.conf import settings
from django.utils import timezone

from django.utils.text import slugify
from django.urls import reverse
import random
import string
from django.contrib.auth import get_user_model

User = get_user_model()

class Forum(models.Model):
    title = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=150)
    slug  = models.SlugField(unique=True)
    icon = models.ImageField(upload_to='forum_icons/', null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Forum, self).save(*args, **kwargs) 

    def get_subforums(self):
        qs = SubForum.objects.filter(forum = self.id)
        return list(qs)

    def __str__(self):
        return 'forum: ' + self.title 

class SubForum(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=150)
    slug = models.SlugField(blank=True)
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ['slug','forum']
       
    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(SubForum, self).save(*args, **kwargs) 

    def get_posts(self):
        qs = Post.objects.filter(subForum = self.id)
        return list(qs)

    def __str__(self):
        return 'SubForum:' + self.title 

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=100, default="default title")
    content = models.TextField()
    upvote = models.ManyToManyField(User,blank=True, default=None, related_name="post_upvote")
    downvote = models.ManyToManyField(User,blank=True, default=None, related_name="post_downvote")
    created_date = models.DateTimeField(default=timezone.now)
    edited_date = models.DateTimeField(blank=True, null=True)
    subForum = models.ForeignKey(SubForum, on_delete=models.CASCADE)
    slug = models.SlugField()
    
    class Meta:
        unique_together = ('subForum','slug')

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs) 
    
    def get_comments(self):
        qs = Comment.objects.filter(post = self.id, parent=None)
        return list(qs)


    def upVote(self, _user):
        self.upvote.add(_user)
        

    def downVote(self, _user):
        self.downvote.add(_user)
       

    def __str__(self):
        return 'post: ' + self.title 



class Comment(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True,on_delete=models.CASCADE,related_name='replies')
    upvote = models.ManyToManyField(User,blank=True,related_name="comment_upvote")
    downvote = models.ManyToManyField(User,blank=True, related_name="comment_downvote")
    created_date = models.DateTimeField(default=timezone.now)
    edited_date = models.DateTimeField(blank=True, null=True)


    class Meta:
        ordering = ['-created_date']

    def children(self):
        return Comment.objects.filter(parent=self).order_by('created_date')
    

    def upVote(self, _user):
        self.upvote.add(user)

    def downVote(self, _user):
        self.downvote.add(user)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    def __str__(self):
        return f'{self.user.username} Comment'


# method used in testing

def create_forum(user, title, description):
    slug = slugify(title)
    if Forum.objects.filter(slug=slug).exists():
        print("forum title already exists")
        return Forum.objects.get(slug=slug)
    else:
        forum = Forum(title=title, description= description, slug = slug, creator = user)
        forum.save()
        return forum

def create_subForum(user, title, description, forum):
    slug = slugify(title)
    if SubForum.objects.filter(slug=slug).exists():
        print('title not unique')
        return SubForum.objects.get(slug=slug)
    subForum = SubForum(creator = user, title = title, description=description, forum=forum, slug=slug)  
    subForum.save()
    return subForum

# methods for post actions
def create_post(user, content, subForum):
    postID = randomString(20)
    while Post.objects.filter(slug=postID).exists():
        postnum = randomString(20)

    post = Post(user=user, content=content, subForum=subForum, slug=postID)
    post.publish()
    post.save()
    return post

def randomString(stringLength):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(stringLength))

    
