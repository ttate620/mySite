from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth.decorators import login_required
from .models import Friend, Profile
from explore.models import Post
import json


@login_required
def account(request):
    template = loader.get_template('account.html')
    context = {
        'content' : 1, 
    }
    
    return HttpResponse(template.render(context, request))

@login_required
def profile(request, pk):
    self_profile = Profile.objects.get(user=request.user)
    user_profile = Profile.objects.get(pk = pk)
    user_friend = Friend.objects.get(current_user_profile=user_profile)
    user_friends_list = user_friend.friend_list()
    status = user_friend.status(self_profile)
    user = request.user
    posts = ['No Posts yet!']
    if Post.objects.filter(user=user):
        posts = Post.objects.filter(user=user)
    content = {
        'self_profile': self_profile,
        'user_profile': user_profile,
        'profile' : user_profile,
        'friendsList': user_friends_list,
        'status' : status,
        'posts':posts,
    }
    return render(request,"profile.html", content )

@login_required
def user_profile(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    profile_pk = profile.pk
    return redirect('account:profile', pk = str(profile.pk))

@login_required
def update_profile(request, pk, profile_field):
    updated_info = request.POST['updated_info']
    profile = Profile.objects.get(pk=pk)
    setattr(profile, profile_field , updated_info)
    profile.save()
   
    return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )
