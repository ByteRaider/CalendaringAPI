from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.conf import settings
    
class Room(models.Model):
    name = models.CharField(max_length=100)
    isActive = models.BooleanField(default=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    def __str__(self):
        return f"{self.name} PK:{self.pk}"

class Chair(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='chairs')
    chair_number = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    isTaken = models.BooleanField(default=False)
    isVIP = models.BooleanField(default=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.chair_number} PK:{self.pk}"
    class Meta:
        ordering = ['chair_number']

    
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
        return f"{self.title} PK:{self.pk}"

    def clean(self):
        # Check if start time is before end time
        if self.start_time >= self.end_time:
            raise ValidationError('Start time must be before end time')
        
        #Check if room is Active
        if not self.room.isActive:
            raise ValidationError({'room': 'The selected room is not active.'})
    
        # Check chair availability -
        if self.content_type.model == 'chair':
            chair = self.content_object
            #check if chair is taken
            if chair.isTaken or not chair.room.isActive:
                raise ValidationError({'chair': 'This chair is not available. Room not active or chair taken'})
            #check chair is a room child
            if chair.room != self.room:
                raise ValidationError({'chair': 'This chair is not in the selected room.'})
            
            # Check overlaping chair pk events
            overlapping_chairs = Event.objects.filter(
                content_type=ContentType.objects.get_for_model(Chair.objects.get(pk=chair.pk)),
                object_id=chair.pk,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            ).exclude(id=self.id)
            if overlapping_chairs.exists():
                raise ValidationError('There is an overlapping event on this chair, please try a different chair or time')
            

            
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
