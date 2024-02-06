from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
    
class Chair(models.Model):
    room = models.ForeignKey('Room', on_delete=models.CASCADE, related_name='chairs')
    chair_number = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    isTaken = models.BooleanField(default=False)
    isVIP = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.chair_number} PK:{self.pk}"
    class Meta:
        ordering = ['chair_number']
class Room(models.Model):
    name = models.CharField(max_length=100)
    isActive = models.BooleanField(default=True)
    def __str__(self):
        return self.name


    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content_type = models.ForeignKey('contenttypes.ContentType', on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey()

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
        
        #Check if room is Active
        if not self.room.isActive:
            raise ValidationError({'room': 'The selected room is not active.'})
    
        # Check chair availability - Adjust accordingly
        if self.content_type.model == 'chair':
            chair = self.content_object
            if chair.isTaken or not chair.room.isActive:
                raise ValidationError({'chair': 'This chair is not available.'})

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
