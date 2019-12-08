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
        fields = ('id', 'user', 'event_type', 'notes', 'event_date')
        read_only_fields = ('id', )


class BovidSerializer(serializers.ModelSerializer):
    """Serializer for bovid object"""

    class Meta:
        model = Bovid
        fields = (
                'id', 'mothers_name', 'fathers_name',
                'type_of_bovid', 'breed', 'name', 'breeder',
                'price', 'date_of_birth', 'date_of_death',
                'date_of_purchase', 'date_sold', 'created',
                'updated', 'tags', 'user')
        read_only_fields = ('id', 'created')


class BovidDetailSerializer(BovidSerializer):
    """Serializer for bovid object"""

    tags = TagSerializer(many=True, read_only=True)


class BovidImageSerializer(serializers.ModelSerializer):
    """Serializer for uploading images to bovine"""

    class Meta:
        model = Bovid
        fields = ('id', 'image')
        read_only_fields = ('id',)
