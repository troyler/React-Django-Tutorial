from django.urls import path
from .views import index

app_name = "frontend"  #this is for django to know this is a front_end app, redirected from spotify/views

urlpatterns = [
    path('', index, name = ""),   #render index template when blank path 
    path('join', index),
    path('create', index),
    path('room/<str:roomCode>', index) #means we will accept a string here after room, if we want it to be an integer, would be int
]
