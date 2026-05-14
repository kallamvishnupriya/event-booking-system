from django.shortcuts import get_object_or_404
from django.db import transaction
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import Booking
from .serializers import BookingSerializer
from events.models import Event


# ---------------- BOOK EVENT ----------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def book_event(request):

    user = request.user

    # ✅ ROLE CHECK (RBAC)
    if hasattr(user, 'role') and user.role not in ['customer', 'organizer', 'manager']:
        return Response(
            {"error": "You are not allowed to book events"},
            status=status.HTTP_403_FORBIDDEN
        )

    event_id = request.data.get("event_id")

    if not event_id:
        return Response(
            {"error": "event_id is required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    event = get_object_or_404(Event, id=event_id)

    with transaction.atomic():

        # 🔥 SOLD OUT CHECK
        if event.is_sold_out:
            return Response(
                {"error": "Event is sold out"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔥 PREVENT DOUBLE BOOKING
        if Booking.objects.filter(user=user, event=event).exists():
            return Response(
                {"error": "Already booked"},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking = Booking.objects.create(
            user=user,
            event=event
        )

    serializer = BookingSerializer(booking)

    return Response(
        {
            "message": "Booked successfully",
            "data": serializer.data
        },
        status=status.HTTP_201_CREATED
    )


# ---------------- MY BOOKINGS ----------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_bookings(request):

    user = request.user

    bookings = Booking.objects.filter(user=user).select_related('event')

    serializer = BookingSerializer(bookings, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)