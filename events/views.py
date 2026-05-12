from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .models import Event
from .serializers import EventSerializer
from users.models import UserProfile
from bookings.models import Booking


# ---------------- GET EVENTS ----------------
@api_view(['GET'])
def get_events(request):
    events = Event.objects.all().order_by('-id')
    serializer = EventSerializer(events, many=True)

    data = serializer.data

    # add booking count
    for i, event in enumerate(events):
        data[i]["booking_count"] = Booking.objects.filter(event=event).count()

    return Response(data)


# ---------------- CREATE EVENT ----------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):

    profile = UserProfile.objects.get(user=request.user)

    if profile.role not in ["organizer", "manager"]:
        return Response(
            {"error": "Only organizers/managers can create events"},
            status=403
        )

    serializer = EventSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


# ---------------- UPDATE EVENT ----------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_event(request, id):

    profile = UserProfile.objects.get(user=request.user)

    if profile.role not in ["organizer", "manager"]:
        return Response(
            {"error": "Permission denied"},
            status=403
        )

    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=404)

    serializer = EventSerializer(event, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


# ---------------- DELETE EVENT ----------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event(request, id):

    profile = UserProfile.objects.get(user=request.user)

    if profile.role not in ["organizer", "manager"]:
        return Response(
            {"error": "Permission denied"},
            status=403
        )

    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=404)

    event.delete()

    return Response({"message": "Event deleted"})


# ---------------- SOLD OUT TOGGLE ----------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_sold_out(request, id):

    profile = UserProfile.objects.get(user=request.user)

    # ONLY MANAGER
    if profile.role != "manager":
        return Response(
            {"error": "Only manager can control sold out"},
            status=403
        )

    try:
        event = Event.objects.get(id=id)
    except Event.DoesNotExist:
        return Response({"error": "Event not found"}, status=404)

    event.is_sold_out = not event.is_sold_out

    event.save(update_fields=["is_sold_out"])

    return Response({
        "message": "Sold out status updated",
        "is_sold_out": event.is_sold_out
    })