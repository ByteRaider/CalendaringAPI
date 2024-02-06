from django.contrib import admin
from .models import Room, Chair, Event

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['id','name', 'isActive', 'chairCount']
    list_per_page = 10
    search_fields = ['name__istartswith']
    list_filter = ['isActive']
    ordering = ['name', 'isActive']

    def get_queryset(self, request):
        # Prefetch the related Chair objects to optimize query performance
        queryset = super().get_queryset(request).prefetch_related('chairs')
        return queryset

    @admin.display(description='Chairs in room')
    def chairCount(self, obj: Room):
        # Since chairs are prefetched, this won't hit the database again
        return f"{obj.chairs.count()} chairs" if obj.chairs.exists() else 'No chairs have been added to this room'
    class Meta:
        ordering = ['name', 'isActive']


@admin.register(Chair)
class ChairAdmin(admin.ModelAdmin):
    pass
    list_display = ['id', 'room', 'chair_number', 'price', 'isTaken', 'isVIP']
    list_filter = ['isTaken', 'isVIP', 'room__name']
    list_editable = ['chair_number', 'price', 'isVIP']
    readonly_fields = ['isTaken']
    ordering = ['room','isTaken', 'isVIP']
    list_select_related = ['room']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
    list_display = ['id', 'title','description','room', 'start_time', 'end_time', 'user', 'room_chairs']
    list_read_only_fields = ['user']
    list_editable = ['title', 'description', 'start_time', 'end_time', 'room']
    ordering = ['room', 'start_time', 'end_time']
    list_filter = ['start_time', 'end_time', 'room__name']
    search_fields = ['title__icontains', 'room__name__icontains', 'user__username__icontains']

    def get_queryset(self, request):
        # Prefetch the related objects to optimize query performance
        queryset = super().get_queryset(request).prefetch_related('room', 'user', 'room__chairs')
        return queryset

    @admin.display(description='Related chair')
    def room_chairs(self, obj):
        return ', '.join([f"Chair ID: {chair.id}, Chair Number: {chair.chair_number}" for chair in obj.room.chairs.all()])
    room_chairs.short_description = 'Related Chairs'