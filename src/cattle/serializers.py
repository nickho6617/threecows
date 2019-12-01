from rest_framework import serializers

from core.models import Tag, LifeEvent


class TagSerializer(serializers.ModelSerializer):
    """Serializer for tag object"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class LifeEventSerializer(serializers.ModelSerializer):
    """Serializer for Life Event object"""

    class Meta:
        model = LifeEvent
        fields = ('id', 'bovid', 'event_type', 'notes', 'event_date')
        read_only_fields = ('id', )
