from .views import RoomView, CreateRoomView, GetRoom, JoinRoom, UserInRoom, LeaveRoom
from django.urls import path

#points to the location of different /api/... path visits and calls views 

urlpatterns = [
    path('room',RoomView.as_view()), #at path 'room' return the RoomView as view 
    path('create-room', CreateRoomView.as_view()),
    path('get-room', GetRoom.as_view()),
    path('join-room', JoinRoom.as_view()),
    path('user-in-room', UserInRoom.as_view()),
    path('leave-room', LeaveRoom.as_view()),

]