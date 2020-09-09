from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from accounts.models import Profile, Friend
from django.utils.text import slugify
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


from .tokens import account_activation_token 
from .forms import UserRegisterForm, PRForm 

User = get_user_model()

def home(request):
    if request.user.is_active:
        return redirect('explore:explore')
    else:
        return redirect('login:login')

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        auth_login(request, user)
        return redirect('login:home')
    else:
        return HttpResponse('Activation link is invalid!')



def register(request):
   if request.method == 'POST':
      form = UserRegisterForm(request.POST)
      if form.is_valid():
         user = form.save(commit=False)
         user.is_active = False
         user.save()
         profile = Profile.objects.create(user=user)
         Friend.objects.create(current_user_profile=profile)
         current_site = get_current_site(request)
         mail_subject = 'Activate your mySite account.'
         message = render_to_string('registration/activate_email.html', {
               'user': user,
               'domain': current_site.domain,
               'uid':urlsafe_base64_encode(force_bytes(user.pk)),
               'token':account_activation_token.make_token(user),
         })
         to_email = form.cleaned_data.get('email')
         email = EmailMessage(
                     mail_subject, message, to=[to_email]
         )
         email.send()
         return render(request,'registration/confirmation_message.html', {})

   else:
      form = UserRegisterForm()
   return render(request,'register.html', {'form': form})

def reset_password(request):
    return render(request,'registration/password_reset_form.html', {})

