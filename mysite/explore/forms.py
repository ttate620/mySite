from django import forms
from .models import Forum, SubForum, Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class ForumCreationForm(forms.Form):
    title = forms.CharField(label='Title',max_length=100)
    description = forms.CharField(label='Description', max_length=150)
    icon = forms.ImageField(label='UploadIcon', required=False)
    
    class Meta:
        model = Forum
        exclude = ['slug','creator']
        
class SubForumCreationForm(forms.Form):
    title = forms.CharField(label='Title',max_length=100)
    description = forms.CharField(label='Description', max_length=150)
    class Meta:
        model = SubForum
        exclude = ['slug','creator','forum']
        
        
class PostCreationForm(forms.ModelForm):
    title = forms.CharField(label='Title',max_length=60)
    content = forms.CharField(widget=forms.Textarea)
    class Meta:
        model = Post
        exclude = ['slug', 'user', 'subForum', 'upvote', 'downvote', 'created_date', 'edited_date']

class CommentCreationForm(forms.ModelForm):
    content = forms.CharField(label=False,widget=forms.Textarea(attrs={'rows':3, 'cols':60}))
    class Meta:
        model = Comment
        exclude = ['upvote', 'downvote', 'created_date', 'edited_date', 'post', 'parent','user']
