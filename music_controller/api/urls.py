from .views import RoomView, CreateRoomView
from django.urls import path

#points to the location of different /api/... path visits and calls views 

urlpatterns = [
    path('room',RoomView.as_view()), #at path 'room' return the RoomView as view 
    path('create-room', CreateRoomView.as_view())

]