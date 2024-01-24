from rest_framework import serializers
from .models import Event, Room, Chair


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class ChairSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chair
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    room = RoomSerializer(read_only=True)
    chair = ChairSerializer(read_only=True)
    class Meta:
        model = Event
        fields = '__all__'