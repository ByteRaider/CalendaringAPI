from django.contrib import admin
from .models import Room, Chair, Event

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'Roomchairs']
    list_per_page = 10
    search_fields = ['name__istartswith']
    #get_chairs for room
    def Roomchairs(self, obj):
        chairs = Chair.objects.filter(room=obj)
        chair_list = ', '.join([str(chair) for chair in chairs])
        return chair_list


@admin.register(Chair)
class ChairAdmin(admin.ModelAdmin):
    pass
    list_display = ['id','room', 'chair_number', 'price', 'isTaken', 'isVIP']
    list_filter = ['room', 'chair_number', 'isTaken', 'isVIP']
    list_editable = ['chair_number', 'price']
    readonly_fields = ['isTaken']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
    list_display = ['id','room', 'start_time', 'end_time']
    list_filter = ['id',    'room', 'start_time', 'end_time']  