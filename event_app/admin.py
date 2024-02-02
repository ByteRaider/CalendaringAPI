from django.contrib import admin
from .models import Room, Chair, Event

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name', 'Roomchairs']
    list_per_page = 10
    #search_fields = ['Roomchairs']
    #get_chairs for room
    def Roomchairs(self, obj):
        chairs = Chair.objects.filter(room=obj)
        chair_list = ', '.join([str(chair) for chair in chairs])
        return chair_list
        #return chairs.values_list('id', flat=True)



@admin.register(Chair)
class ChairAdmin(admin.ModelAdmin):
    pass
    list_display = ('id','room', 'price', 'isTaken', 'isVIP')
    list_filter = ('id','room', 'isTaken', 'isVIP')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
    list_display = ('id','room', 'start_time', 'end_time')
    list_filter = ('id','room', 'start_time', 'end_time')    