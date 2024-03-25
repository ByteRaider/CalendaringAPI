from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError
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
    class Meta:
        model = Event
        fields = '__all__'

    def validate(self, attrs):
        instance = Event(**attrs)
        try:
            instance.clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)
        return attrs

    def create(self, validated_data):
        event = Event.objects.create(**validated_data)
        try:
            event.clean()
        except DjangoValidationError as e:
            event.delete()  # Rollback the creation
            raise ValidationError(e.message_dict)
        return event

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        try:
            instance.clean()
        except DjangoValidationError as e:
            raise ValidationError(e.message_dict)
        return instance