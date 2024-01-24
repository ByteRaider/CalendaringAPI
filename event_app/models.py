from django.db import models
from django.core.exceptions import ValidationError

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

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

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)