from rest_framework import serializers

from core.models import Tag, LifeEvent, Bovid


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


class BovidSerializer(serializers.ModelSerializer):
    """Serializer for bovid object"""

    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Bovid
        fields = (
            'mothers_name', 'fathers_name', 'type_of_bovid', 'breed',
            'name', 'breeder', 'price', 'date_of_birth', 'date_of_death',
            'date_of_purchase', 'date_sold', 'created', 'updated', 'tags',
            'user'
        )
        read_only_fields = ('id', 'created')
