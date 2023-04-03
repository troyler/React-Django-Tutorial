from django.urls import path
from .views import index

urlpatterns = [
    path('', index),   #render index template when blank path 
    path('join', index),
    path('create', index),
    path('room/<str:roomCode>', index) #means we will accept a string here after room, if we want it to be an integer, would be int
]
