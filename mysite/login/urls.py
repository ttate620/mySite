from django.urls import path, include
from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views
from . import views
app_name="login"

urlpatterns = [
    url(r'^$', views.home, name="home"),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    url(r'^register/$', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.activate, name='activate'),
    path('activate/<str:uidb64>/<str:token>/',
        views.activate, name='activate'),
    url(r'^password-reset/$', auth_views.PasswordResetView.as_view(template_name="registration/password_reset_form.html"), name="reset_password"),
    url(r'^password-reset/done/$', 
        auth_views.PasswordResetDoneView.as_view(template_name="registration/password_reset_done.html"),name="password_reset_done"),
    url(r'^password-reset-confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    auth_views.PasswordResetConfirmView.as_view(template_name="registration/password_reset_confirm.html"),name="password_reset_confirm"),
    url(r'^password-reset-complete/$', auth_views.PasswordResetCompleteView.as_view(template_name="registration/password_reset_complete.html"), name="password_reset_complete"),

]
# auth_views.LoginView.as_view()