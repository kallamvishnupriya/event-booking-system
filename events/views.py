from django.shortcuts import get_object_or_404

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Event
from .serializers import EventSerializer
from users.models import UserProfile
from django.db.models import Count


# ---------------- GET EVENTS ----------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_events(request):

    user = request.user

    events = Event.objects.annotate(
        booked_count=Count('booking')
    ).order_by('-id')

    data = []

    for event in events:

        is_booked = False

        if user.is_authenticated:
            is_booked = event.booking_set.filter(user=user).exists()

        data.append({
            "id": event.id,
            "title": event.title,
            "description": event.description,
            "date": event.date,
            "location": event.location,
            "capacity": event.capacity,
            "is_sold_out": event.is_sold_out,
            "booked_count": event.booked_count,
            "is_booked": is_booked
        })

    return Response(data)


# ---------------- CREATE EVENT ----------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_event(request):

    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role not in ["organizer", "manager"]:
        return Response(
            {"error": "Only organizers/managers can create events"},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = EventSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- UPDATE EVENT ----------------
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_event(request, id):

    profile = get_object_or_404(UserProfile, user=request.user)
    event = get_object_or_404(Event, id=id)

    # 🔥 ownership check
    if profile.role == "organizer" and event.created_by != request.user:
        return Response(
            {"error": "You can only edit your own events"},
            status=status.HTTP_403_FORBIDDEN
        )

    if profile.role not in ["organizer", "manager"]:
        return Response(
            {"error": "Permission denied"},
            status=status.HTTP_403_FORBIDDEN
        )

    serializer = EventSerializer(event, data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- DELETE EVENT ----------------
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_event(request, id):

    profile = get_object_or_404(UserProfile, user=request.user)
    event = get_object_or_404(Event, id=id)

    # 🔥 ownership check
    if profile.role == "organizer" and event.created_by != request.user:
        return Response(
            {"error": "You can only delete your own events"},
            status=status.HTTP_403_FORBIDDEN
        )

    if profile.role not in ["organizer", "manager"]:
        return Response(
            {"error": "Permission denied"},
            status=status.HTTP_403_FORBIDDEN
        )

    event.delete()

    return Response(
        {"message": "Event deleted"},
        status=status.HTTP_200_OK
    )


# ---------------- SOLD OUT TOGGLE ----------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def toggle_sold_out(request, id):

    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.role != "manager":
        return Response(
            {"error": "Only manager can control sold out"},
            status=status.HTTP_403_FORBIDDEN
        )

    event = get_object_or_404(Event, id=id)

    event.is_sold_out = not event.is_sold_out
    event.save(update_fields=["is_sold_out"])

    return Response(
        {
            "message": "Sold out status updated",
            "is_sold_out": event.is_sold_out
        },
        status=status.HTTP_200_OK
    )