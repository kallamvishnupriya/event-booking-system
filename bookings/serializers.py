from rest_framework import serializers
from .models import Booking


class BookingSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(
        source='event.title',
        read_only=True
    )

    class Meta:
        model = Booking
        fields = [
            'id',
            'event',
            'event_title',
            'booked_at',
        ]