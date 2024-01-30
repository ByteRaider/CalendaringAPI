from django.contrib import admin
from .models import Room, Chair, Event

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass
   # list_display = ('name', 'chairs')
@admin.register(Chair)
class ChairAdmin(admin.ModelAdmin):
    pass
   # list_display = ('room', 'number', 'price', 'isTaken', 'isVIP')
   # list_filter = ('room', 'isTaken', 'isVIP')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
    #list_display = ('room', 'chair', 'start_time', 'end_time')
    #list_filter = ('room', 'chair')