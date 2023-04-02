from django.urls import path
from .views import index

urlpatterns = [
    path('', index),   #render index template when blank path 
    path('join', index),
    path('create', index),
    path('room/<str:roomCode>', index)
]
