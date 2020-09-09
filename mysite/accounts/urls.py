from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^profile/(?P<pk>\d+)/update/(?P<profile_field>.+)/$', views.update_profile, name='update_profile'),
    path('', views.account, name="accounts"),
    path('profile/<str:pk>/', views.profile, name="profile"),
    path('profile/', views.user_profile, name="user_profile"),
]