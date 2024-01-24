from rest_framework import viewsets
from .models import Tag, TaggedItem
from .serializers import TagSerializer, TaggedItemSerializer

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class TaggedItemViewSet(viewsets.ModelViewSet):
    queryset = TaggedItem.objects.all()
    serializer_class = TaggedItemSerializer
