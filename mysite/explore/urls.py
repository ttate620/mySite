from django.urls import path, include
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.explore, name="explore"),
    url(r'^connect/(?P<operation>.+?)/(?P<pk>\d+?)/$', views.change_friend_status, name='change_friend_status'),
    url(r'^(?P<slug>[-\w]+)/$', views.forum, name="forum"),
    url(r'^(?P<slug1>[-\w]+)/(?P<slug2>[-\w]+)/$', views.subforum, name="subforum"),
    url(r'^(?P<slug1>[-\w]+)/(?P<slug2>[-\w]+)/(?P<slug3>[-\w]+)/$', views.post, name="post"),
    path('like/', views.like, name="like"),
    #path('<slug:slug>/', views.forum, name="forum"),
    #path('<slug:slug1>/<slug:slug2>/', views.subforum, name="subforum"),
    #path('<slug:slug1>/<slug:slug2>/<slug:slug3>/',views.post, name="post"),
    

    
]