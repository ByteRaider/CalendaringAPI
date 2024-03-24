from django.forms import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Room, Chair, Event

class setupTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        # Create a room
        self.room = Room.objects.create(name='Test Room', isActive=True, user=self.user)
        # Create a chair
        self.chair = Chair.objects.create(room=self.room, chair_number=1, price=100, isVIP=True, user=self.user)
        print(self.user, "Setup complete.")

    def test_create_room(self):
        self.assertEqual(self.room.name, 'Test Room')
        print(self.room, "Created successfully by user: ", self.user)
    
    def test_assing_chair2Room(self):
        self.assertEqual(self.chair.chair_number, 1)
        print(self.chair, "Created successfully in room: ", self.room)

    def test_create_event(self):
        event = Event.objects.create(
            title='Test Event',
            description='Test Description',
            room=self.room, 
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(hours=1),
            user=self.user,
            content_type=ContentType.objects.get_for_model(Chair),
            object_id=self.chair.pk
        )
        self.assertEqual(event.title, 'Test Event')
        self.assertEqual(event.description, 'Test Description')
        self.assertEqual(event.room, self.room)
        # Comparing timezones directly may lead to issues due to precision differences; consider using a range or delta for comparison instead.
        self.assertTrue(abs(event.start_time - timezone.now()) < timezone.timedelta(seconds=1))
        self.assertTrue(abs((event.end_time - (timezone.now() + timezone.timedelta(hours=1))) < timezone.timedelta(seconds=1)))
        self.assertEqual(event.user, self.user)
        self.assertEqual(event.content_type, ContentType.objects.get_for_model(Chair))
        self.assertEqual(event.object_id, self.chair.pk)