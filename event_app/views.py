from rest_framework.exceptions import ValidationError
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import ValidationError as DjangoValidationError
from django.utils.timezone import make_aware
from datetime import datetime
from .models import Event, Room, Chair
from .serializers import EventSerializer, RoomSerializer, ChairSerializer
# for development only, delete next 2 lines for propduction -- IMPORTANT! -- IMPORTANT!-- IMPORTANT!
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# for development only, delete PREVIOUS 2 lines for propduction -- IMPORTANT! -- IMPORTANT!-- IMPORTANT!

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ChairViewSet(viewsets.ModelViewSet):
    queryset = Chair.objects.all()
    serializer_class = ChairSerializer
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@method_decorator(csrf_exempt, name='dispatch')
class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        # Get room and date from request query parameters
        room = self.request.query_params.get('room')
        date = self.request.query_params.get('date')

        # Filter by room if provided
        if room is not None:
            queryset = queryset.filter(room__id=room)
        #return queryset.prefetch_related('room', 'room__chairs')
        return queryset.prefetch_related('room')
    

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            # Custom validation logic can be placed here
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except DjangoValidationError as e:
            # Handling Django's ValidationError
            return Response({"detail": e.messages}, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer):
        # Add any custom creation logic here
        
        serializer.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        try:
            # Custom validation logic can be placed here
            self.perform_update(serializer)
            return Response(serializer.data)
        except DjangoValidationError as e:
            # Handling Django's ValidationError
            return Response({"detail": e.messages}, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        # Add any custom update logic here
        serializer.save()