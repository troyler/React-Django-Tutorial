from .models import SpotifyToken
from django.utils import timezone
from datetime import timedelta
from .credentials import CLIENT_ID, CLIENT_SECRET
from requests import post, put, get


BASE_URL = "https://api.spotify.com/v1/me/"


def get_user_tokens(session_id):
    user_tokens = SpotifyToken.objects.filter(user=session_id)

    if user_tokens.exists():
        return user_tokens[0]
    else:
        return None


def update_or_create_user_tokens(session_id, access_token, token_type, expires_in, refresh_token):
    tokens = get_user_tokens(session_id)
    expires_in = timezone.now() + timedelta(seconds=expires_in)

    if tokens:
        tokens.access_token = access_token
        tokens.refresh_token = refresh_token
        tokens.expires_in = expires_in
        tokens.token_type = token_type
        tokens.save(update_fields=['access_token',
                                   'refresh_token', 'expires_in', 'token_type'])
    else:
        tokens = SpotifyToken(user=session_id, access_token=access_token,
                              refresh_token=refresh_token, token_type=token_type, expires_in=expires_in)
        tokens.save()


def is_spotify_authenticated(session_id):
    tokens = get_user_tokens(session_id)
    if tokens:
        expiry = tokens.expires_in
        if expiry <= timezone.now():
            refresh_spotify_token(session_id)

        return True

    return False


def refresh_spotify_token(session_id):
    refresh_token = get_user_tokens(session_id).refresh_token

    response = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')

    update_or_create_user_tokens(
        session_id, access_token, token_type, expires_in, refresh_token)


def execute_spotify_api_request(session_id, endpoint, post_=False, put_=False):   #takes session_id (host token here), endpoints, request type
    tokens = get_user_tokens(session_id)   #set the tokens from the session_id
    headers = {'Content-Type': 'application/json',    #some stuff for spotify
               'Authorization': "Bearer " + tokens.access_token}   #Bearer must have space following it

    if post_:    #if we set post to be true, sends post request 
        post(BASE_URL + endpoint, headers=headers)
    if put_:      #if we set put to be true, same deal
        put(BASE_URL + endpoint, headers=headers)

    response = get(BASE_URL + endpoint, {}, headers=headers)  #if we did not set either to be true,we assume a get request
    #{} is what we are sending with the request, excpet here we just send nothing for syntax 
    try:
        return response.json()  #attempt to return the response of the response 
    except:
        return {'Error': 'Issue with request'}
    
# did not include try, except block for the other requests because we do not care about their responses 

def play_song(session_id):
    print("song playing")
    return execute_spotify_api_request(session_id, "player/play", put_ = True)



def pause_song(session_id):
    print("song paused")
    return execute_spotify_api_request(session_id, "player/pause", put_ = True)