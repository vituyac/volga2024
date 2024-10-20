from rest_framework import serializers
from .models import *
    
    
class TimetableSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Timetable
        fields = ('id', 'hospitalId', 'doctorId', 'fr', 'to', 'room')
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['from'] = representation.pop('fr')
        return representation
    
    def to_internal_value(self, data):
        if 'from' in data:
            data['fr'] = data.pop('from')
        return super().to_internal_value(data)
    
class TicketSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Ticket
        fields = ('id', 'time',)
    