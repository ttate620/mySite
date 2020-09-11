from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Forum, SubForum, Post, Comment
from django.contrib.auth import get_user_model
import json
from django.contrib import messages
from accounts.models import Friend, Profile
from .forms import ForumCreationForm, SubForumCreationForm, PostCreationForm, CommentCreationForm
from django.contrib.auth.decorators import login_required
User = get_user_model()

@login_required
def change_friend_status(request, operation, pk):
    user_profile = Profile.objects.get(user = request.user)
    friend_profile = Profile.objects.get(pk=pk)
    if user_profile != friend_profile:
        if operation == 'add' or operation == 'accept':
            Friend.make_friend(user_profile, friend_profile)

        else:
            Friend.remove_friend(user_profile, friend_profile)

        return JsonResponse({'success':'True'})
    return JsonResponse({'success':'False'})
@login_required
def explore(request):
    if request.method == 'POST':
        form = ForumCreationForm(request.POST.copy())
        form.data['creator'] = request.user
        if form.is_valid():
            try:
                newForum = Forum(title = form.data['title'], description = form.data['description'],creator = form.data['creator'])
                icon = form.data['icon']
                if icon:
                    newForum.icon = icon
                newForum.save()
                return redirect('explore:forum', newForum.slug)
            except Exception as e:
                messages.warning(request, f'Forum title must be unique')
                return redirect("explore:explore")

    profiles = Profile.get_random(10)
    user_profile = Profile.objects.get(user = request.user)
    friend = Friend.objects.get(current_user_profile = user_profile)
    userFr = friend.friend_list()
    requested = friend.request_sent()
    requests = friend.request_sent_to_me()
   
    context = {
        'forums' : Forum.objects.all(), 
        'profiles':profiles,
        'user_profile': user_profile,
        'friends' : userFr,
        'requested': requested,
        'requests': requests,
        'forumForm': ForumCreationForm()
    } 
    return render(request, 'explore.html', context)

@login_required
def forum(request, slug):
    forum = Forum.objects.get(slug=slug)
    if request.method == 'POST':
        form = SubForumCreationForm(request.POST.copy()) 
        form.data['forum'] = forum
        form.data['creator'] = request.user
        if form.is_valid():
            try:
                newSubForum = SubForum(
                    forum = form.data['forum'], 
                    title = form.data['title'], 
                    description = form.data['description'],
                    creator = form.data['creator']
                    )
                
                newSubForum.save()
                print("created successfully")
                return redirect('explore:subforum',slug1 = slug, slug2 = newSubForum.slug)
            except Exception as e:
                print("error ",e)
                messages.warning(request, f'Subforum title must be unique')
                return redirect("explore:forum", slug)

    subforums = forum.get_subforums()
    newForm = SubForumCreationForm()
    context = {
        'forum': forum,
        'subforums' : subforums, 
        'subforumForm': newForm,
    }
    return render(request,"forum.html",context)

@login_required
def subforum(request, slug1, slug2):
    forum = Forum.objects.get(slug=slug1)
    subforum = SubForum.objects.get(slug=slug2, forum=forum)
    if request.method == 'POST':
        form = PostCreationForm(request.POST.copy()) 
        form.data['subForum'] = subforum
        form.data['user'] = request.user
        if form.is_valid():
            try:
                newPost = Post(
                    subForum = form.data['subForum'], 
                    title = form.data['title'], 
                    content = form.data['content'],
                    user = form.data['user']
                    )
                newPost.save()
                return redirect('explore:post',slug1 = slug1, slug2 = slug2, slug3 = newPost.slug)
            except Exception as e:
                messages.warning(request, f'Post title must be unique')
                return redirect("explore:subforum", slug1, slug2)
    posts = subforum.get_posts()
    postForm = PostCreationForm()
    context = {
        'forum': forum,
        'subforum' : subforum, 
        'posts': posts,
        'postForm': postForm,
    }
    return render(request, "subforum.html", context)
    
@login_required
def post(request, slug1, slug2, slug3):
   
    forum = get_object_or_404(Forum, slug=slug1)
    subforum = get_object_or_404(SubForum, slug=slug2, forum=forum)
    post = get_object_or_404(Post, slug=slug3, subForum=subforum)
    comments = post.get_comments()
    if request.method == 'POST':
        comment_form = CommentCreationForm(request.POST.copy())
        if comment_form.is_valid():
            parent_obj = None
            try:
                parent_id = int(request.POST.get('parent_id'))
            except:
                parent_id = None
            reply_comment = comment_form.save(commit=False)
            if parent_id:
                parent_obj = Comment.objects.get(id=parent_id)
                reply_comment.parent = parent_obj
                
            reply_comment.user = request.user
            reply_comment.post = post
            reply_comment.save()
            return redirect('explore:post',slug1 = slug1, slug2 = slug2, slug3 = slug3)
    
    else:
        comment_creation_form = CommentCreationForm()
        
    context = {
        'forum': forum,
        'subforum' : subforum, 
        'post': post,
        'comments': comments,
        'comment_form': comment_creation_form,
        
    }
    
    return render(request, "post.html", context)

@require_POST
@login_required
def like(request):
    user = request.user
    post_id = request.POST['post_id']
    liked = int(request.POST['liked'])
    votes = 0
    post = Post.objects.get(id=post_id)
    if liked == 1:
        post.upVote(user)
        votes = post.upvote.count()
    else:
        post.downVote(user)
        votes=post.downvote.count()

    data = {
        "liked": liked,
        "votes": votes
    }
    return JsonResponse(data)
