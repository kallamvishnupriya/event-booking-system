from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile


# ---------------- REGISTER ----------------
@api_view(["POST"])
def register(request):

    username = request.data.get("username")
    password = request.data.get("password")
    role = request.data.get("role", "customer").lower()

    # ❌ prevent manager creation from frontend
    if role == "manager":
        return Response(
            {"error": "Manager role not allowed"},
            status=status.HTTP_403_FORBIDDEN
        )

    # validation
    if not username or not password:
        return Response(
            {"error": "Username and password required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if role not in ["customer", "organizer"]:
        return Response(
            {"error": "Invalid role"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # duplicate check
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "User already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.create_user(
            username=username,
            password=password
        )

        # ✅ SET ROLE PROPERLY
        profile = user.userprofile
        profile.role = role
        profile.save()

        return Response({
            "message": "User registered successfully"
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ---------------- LOGIN ----------------
@api_view(["POST"])
def login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:

        refresh = RefreshToken.for_user(user)

        # ✅ USE UserProfile ROLE (single source of truth)
        try:
            role = user.userprofile.role
        except UserProfile.DoesNotExist:
            role = "customer"

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": role,
            "username": user.username
        })

    return Response(
        {"error": "Invalid credentials"},
        status=status.HTTP_400_BAD_REQUEST
    )