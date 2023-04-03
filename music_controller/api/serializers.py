from rest_framework import serializers
from .models import Room 
#serializers take models (remember, similar to tables) and turns them into a JSON format

class RoomSerializer(serializers.ModelSerializer):   
    class Meta:
        model = Room
        fields = ('id', 'code', 'host', 'guest_can_pause', 'votes_to_skip', 'created_at')   #why the if if not defined in Room model? 
                                                                                            #It is a unique identifier, automatically created at Room instantiation

class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip')


class UpdateRoomSerializer(serializers.ModelSerializer):
    code = serializers.CharField(validators = [])

    class Meta:
        model = Room
        fields = ('guest_can_pause', 'votes_to_skip', 'code')


#class CreateFuellCellTest(serializers.ModelSerializer):
