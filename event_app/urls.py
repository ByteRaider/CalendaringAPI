from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, ChairViewSet, EventViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet)
router.register(r'chairs', ChairViewSet)
router.register(r'events', EventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
