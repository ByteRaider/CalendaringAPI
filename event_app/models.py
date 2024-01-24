from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
    
class Room(models.Model):
    name = models.CharField(max_length=100)
    chairs = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name

class Chair(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    number = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    isTaken = models.BooleanField(default=False)
    isVIP = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.room.name} Chair {self.number}"
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    chair = models.ForeignKey(Chair, on_delete=models.CASCADE, null=True, blank=True)
    #content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    #object_id = models.PositiveIntegerField()
    #content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return self.title

    def clean(self):
        # Check for overlapping events
        overlapping_events = Event.objects.filter(
            start_time__lt=self.end_time, 
            end_time__gt=self.start_time
        ).exclude(id=self.id)

        if overlapping_events.exists():
            raise ValidationError('There is an overlapping event, please try a different time')

        # Check if the room and chair are available
        if Event.objects.filter(
            room=self.room, 
            chair=self.chair, 
            start_time__lt=self.end_time, 
            end_time__gt=self.start_time
        ).exclude(id=self.id).exists():
            raise ValidationError('The selected room and chair are not available.')

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
