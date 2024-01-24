from django.forms import ValidationError
from django.test import TestCase
from django.utils import timezone
from .models import Event

class EventModelTest(TestCase):
    def test_event_overlap(self):
        # Create an event
        Event.objects.create(
            title="Test Event 1",
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=2)
        )

        # Try to create an overlapping event
        with self.assertRaises(ValidationError):
            Event.objects.create(
                title="Test Event 2",
                start_time=timezone.now() + timezone.timedelta(hours=1),
                end_time=timezone.now() + timezone.timedelta(hours=3)
            )
