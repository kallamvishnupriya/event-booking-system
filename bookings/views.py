from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Booking
from events.models import Event


# ---------------- BOOK EVENT ----------------
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def book_event(request):

    event_id = request.data.get("event_id")

    try:
        event = Event.objects.get(id=event_id)
    except:
        return Response(
            {"error": "Event not found"},
            status=404
        )

    # 🔥 SOLD OUT CHECK
    if event.is_sold_out:
        return Response(
            {"error": "Event is sold out"},
            status=400
        )

    # already booked
    already_booked = Booking.objects.filter(
        user=request.user,
        event=event
    ).exists()

    if already_booked:
        return Response(
            {"error": "Already booked"},
            status=400
        )

    Booking.objects.create(
        user=request.user,
        event=event
    )

    return Response({
        "message": "Booked successfully"
    })


# ---------------- MY BOOKINGS ----------------
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_bookings(request):

    bookings = Booking.objects.filter(user=request.user)

    data = []

    for b in bookings:

        data.append({
            "id": b.id,
            "event_title": b.event.title,
            "booked_at": b.booked_at
        })

    return Response(data)