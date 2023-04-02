from django.db import models
import string
import random 
#'models' are essentially just like tables in a normal database

def generate_unique_code():
    length = 6
    
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k= length))  #generates a random code of k length with only ASCII uppercase characters
        if Room.objects.filter(code=code).count() == 0:   #filters all room objects, checks if code already exists
            break       #if it does not exist, break and return code

    return code
    
    # Create your models here.

class Room(models.Model):
    code = models.CharField(max_length = 8, default=generate_unique_code, unique = True)  #constraints on this field
    host = models.CharField(max_length=50, unique= True)
    guest_can_pause = models.BooleanField(null = False, default= False)
    votes_to_skip = models.IntegerField(null=False, default=1)
    created_at = models.DateTimeField(auto_now_add = True)

#class FuelCellTest(models.Model):
    # uniqueIdentifier = models.CharField(max_length = 8, default=generate_unique_code, unique = True)
    # testClassification = models.CharField(max_length = 20)
    # created_at = models.DateTimeField(auto_now_add = True)
