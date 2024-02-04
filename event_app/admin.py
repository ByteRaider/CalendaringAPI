from django.contrib import admin
from .models import Room, Chair, Event

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_per_page = 10
    search_fields = ['name__istartswith']

    # A function to display a list of chairs in a room. Takes a Chair object as a parameter and returns a list of chairs filtered by the room attribute.
    def get_chairs_in_room(self, room: Room): 
        chairs = Chair.objects.filter(room=room)
        return chairs
    #get_chairs for room
 #   def roomChairs(self, obj: Room):
 #       chairs = Chair.objects.filter(room=obj)
 #       chair_list = ', '.join([str(chair) for chair in chairs])
 #       return chair_list
 # 
 #   @admin.display(description='Chairs')
 #   def chair_list(self, Chair: Chair):
 #       chairs = Chair.objects.filter(room=Chair)
 #       return chairs
 #   class Meta:
 #       ordering = ['Chair__chair_number']


@admin.register(Chair)
class ChairAdmin(admin.ModelAdmin):
    pass
    list_display = ['id','chair_number', 'price', 'isTaken', 'isVIP']
    list_filter = ['chair_number', 'isTaken', 'isVIP']
    list_editable = ['chair_number', 'price']
    readonly_fields = ['isTaken']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
    list_display = ['id','room', 'start_time', 'end_time']
    list_filter = ['id', 'room', 'start_time', 'end_time']  