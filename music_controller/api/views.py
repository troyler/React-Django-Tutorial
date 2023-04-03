from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from .models import Room 
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse


# Views let us view the different API endpoints
# allows for POST and GET Requests, 

class RoomView(generics.ListAPIView):   #returns a view that is already setup to return endpoint data
    queryset = Room.objects.all()  #queryset gets all the Room objects
    serializer_class = RoomSerializer   #this turns all of that data into JSON format

class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'code'

    def get(self, request, format = None):
        code = request.GET.get(self.lookup_url_kwarg)
        if code != None:
            room = Room.objects.filter(code = code)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data  #passing room[0] to serializer to make sure it is valid, then setting data equal to the data of it 
                data['is_host'] = self.request.session.session_key == room[0].host
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Room Not Found': 'Invalid Room Code.'}, status = status.HTTP_404_NOT_FOUND)
        
        return Response({'Bad Request': 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)

class JoinRoom(APIView):
    lookup_url_kwarg = 'code'

    def post(self, request, format = None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()     
        
        code = request.data.get(self.lookup_url_kwarg)
        if code!= None:
            room_result = Room.objects.filter(code=code)
            if len(room_result) > 0:
                room = room_result[0]
                self.request.session['room_code'] = code    #this tells us that the user in this current session is in this room, this is just stored in a users session 
                return Response({'message': 'Room Joined!'}, status=status.HTTP_200_OK)
            return Response({'Bad Request' : 'Inavlid room code'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'Bad Request' : 'Inavlid post data, did not find a code key'}, status=status.HTTP_400_BAD_REQUEST)

        



class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format = None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()
        
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            if queryset.exists():
                room = queryset[0]
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields = ['guest_can_pause', 'votes_to_skip'])
                self.request.session['room_code'] = room.code  
                return Response(RoomSerializer(room).data, status = status.HTTP_200_OK)
            else:
                room = Room(host = host, guest_can_pause = guest_can_pause, votes_to_skip = votes_to_skip)
                room.save()
                self.request.session['room_code'] = room.code  
                return Response(RoomSerializer(room).data, status = status.HTTP_201_CREATED)
            
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)
            
class UserInRoom(APIView):
    def get(self, request, format = None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()     
        data = {
            'code': self.request.session.get('room_code')  #getting the code info deom the session 
        }
        return JsonResponse(data, status = status.HTTP_200_OK)
    
class LeaveRoom(APIView):
    def post(self, request, format = None):
        if 'room_code' in self.request.session:
            self.request.session.pop('room_code')
            host_id = self.request.session.session_key
            room_results = Room.objects.filter(host=host_id)
            if len(room_results) > 0:
                room = room_results[0]
                room.delete()
        
        return Response({'Message': 'Success'}, status=status.HTTP_200_OK)
    
class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer


    def patch(self, request, format = None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create() 
        serializer = self.serializer_class(data = request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            code = serializer.data.get("code")

            queryset = Room.objects.filter(code=code)
            if not queryset.exists():
                return Response({"Message" : "Room not found"}, status=status.HTTP_404_NOT_FOUND)
            
            room = queryset[0]
            user_id = self.request.session.session_key
            if room.host != user_id:
                return Response({"Message": "You are not the host of this room"}, status=status.HTTP_403_FORBIDDEN)
            
            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=["guest_can_pause", "votes_to_skip"])
            return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)


          
         
        return Response({'Bad Request': 'Invalid Data....'}, status=status.HTTP_400_BAD_REQUEST)