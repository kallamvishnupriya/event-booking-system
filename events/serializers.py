from rest_framework import serializers
from .models import Event


class EventSerializer(serializers.ModelSerializer):

    booked_count = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = '__all__'

    def get_booked_count(self, obj):
        return obj.booking_set.count()