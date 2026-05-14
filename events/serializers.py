from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):

    booked_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = '__all__'