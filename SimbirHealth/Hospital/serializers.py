from rest_framework import serializers
from .models import *
    
    
class HospitalSerializer(serializers.ModelSerializer):
    rooms = serializers.SerializerMethodField()
    
    class Meta:
        model = Hospital
        fields = ('id', 'name', 'address', 'contactPhone', 'rooms')
        
    def get_rooms(self, obj):
        return [room.number for room in obj.rooms.all()]
    


