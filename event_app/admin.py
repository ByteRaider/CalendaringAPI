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
    list_display = ['id','chair_number', 'price', 'isTaken', 'isVIP']
    list_filter = ['chair_number', 'isTaken', 'isVIP']
    list_editable = ['chair_number', 'price']
    readonly_fields = ['isTaken']


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass
    list_display = ['id','room', 'start_time', 'end_time']
    list_filter = ['id', 'room', 'start_time', 'end_time']  