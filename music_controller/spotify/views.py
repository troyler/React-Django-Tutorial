from django.shortcuts import render, redirect
from .credentials import REDIRECT_URI, CLIENT_SECRET, CLIENT_ID
from rest_framework.views import APIView
from requests import Request, post
from rest_framework import status
from rest_framework.response import Response
from .util import *
from api.models import Room


class AuthURL(APIView):
    def get(self, request, fornat=None):
        scopes = 'user-read-playback-state user-modify-playback-state user-read-currently-playing'

        url = Request('GET', 'https://accounts.spotify.com/authorize', params={
            'scope': scopes,
            'response_type': 'code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID
        }).prepare().url

        return Response({'url': url}, status=status.HTTP_200_OK)


def spotify_callback(request, format=None):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')
    error = response.get('error')

    if not request.session.exists(request.session.session_key):
        request.session.create()

    update_or_create_user_tokens(
        request.session.session_key, access_token, token_type, expires_in, refresh_token)

    return redirect('frontend:')


class IsAuthenticated(APIView):
    def get(self, request, format=None):
        is_authenticated = is_spotify_authenticated(
            self.request.session.session_key)
        return Response({'status': is_authenticated}, status=status.HTTP_200_OK)


class CurrentSong(APIView):     
    def get(self, request, format=None):   
        room_code = self.request.session.get('room_code')   #getting the room code from the session
        room = Room.objects.filter(code=room_code)   #filtering to find the right room by room_code
        if room.exists():   #if the room exists
            room = room[0]  #it is the first room in the list of rooms 
        else:
            return Response({}, status=status.HTTP_404_NOT_FOUND)   #otherwise, the room does not exist and return a 404 error
        host = room.host    # if it does exist, set the host = room.host
        endpoint = "player/currently-playing" #this is the spotify endpoint we must hit
        response = execute_spotify_api_request(host, endpoint)   #we then pass this to our util function
                                                                 #which performs a get request and returns a json response if valid, and an error if not

        if 'error' in response or 'item' not in response: #checks this reponse for error signifiers
            return Response({}, status=status.HTTP_204_NO_CONTENT)   #return no content if error in request

        item = response.get('item')     #set these different variables equal to the different itms in the response
        duration = item.get('duration_ms')
        progress = response.get('progress_ms')
        album_cover = item.get('album').get('images')[0].get('url')     #getting the album image url, making it easy to display
        is_playing = response.get('is_playing')
        song_id = item.get('id')

        artist_string = ""  #now the artist string may vary if there are multiple artists on a song

        for i, artist in enumerate(item.get('artists')):   #get the dictionary of artists, and enumerate each dictionary within it
            if i > 0: # if there is more than one key pair
                artist_string += ", "   #add a comma to our string
            name = artist.get('name')  #access the name of the artist in the dictionary
            artist_string += name #add the name to the string 

        song = {    #making a custom dictionary to send with all of the data we selected from this response to this request 
            'title': item.get('name'),
            'artist': artist_string,     
            'duration': duration,   #length of the song
            'time': progress,     # shows where the song is currently at 
            'image_url': album_cover,    #this will just be a link to an image 
            'is_playing': is_playing,  #boolean 
            'votes': 0,
            'id': song_id
        }

        return Response(song, status=status.HTTP_200_OK)
    


class PauseSong(APIView):
    def put(self, request, format = None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(code = room_code)[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            pause_song(room.host)
            return Response({}, status = status.HTTP_204_NO_CONTENT)
        
        return Response({}, status = status.HTTP_403_FORBIDDEN)
    


class PlaySong(APIView):
    def put(self, request, format = None):
        room_code = self.request.session.get("room_code")
        room = Room.objects.filter(code = room_code)[0]
        if self.request.session.session_key == room.host or room.guest_can_pause:
            play_song(room.host)
            return Response({}, status = status.HTTP_204_NO_CONTENT)
        
        return Response({}, status = status.HTTP_403_FORBIDDEN)