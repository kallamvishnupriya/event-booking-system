from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from .models import UserProfile


# ---------------- REGISTER ----------------
@api_view(["POST"])
def register(request):

    username = request.data.get("username")
    password = request.data.get("password")
    role = request.data.get("role", "customer")

    # prevent public manager creation
    if role == "manager":
        return Response(
            {"error": "Manager role not allowed"},
            status=403
        )

    # validation
    if not username or not password:
        return Response(
            {"error": "Username and password required"},
            status=400
        )

    # duplicate user check
    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "User already exists"},
            status=400
        )

    try:
        # create auth user
        user = User.objects.create_user(
            username=username,
            password=password
        )

        # create profile
        UserProfile.objects.create(
            user=user,
            role=role
        )

        return Response({
            "message": "User registered successfully"
        })

    except Exception as e:
        print(e)

        return Response(
            {"error": str(e)},
            status=500
        )


# ---------------- LOGIN ----------------
@api_view(["POST"])
def login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(
        username=username,
        password=password
    )

    if user is not None:

        refresh = RefreshToken.for_user(user)

        # default role
        role = "customer"

        # safely get profile role
        try:
            role = user.userprofile.role
        except:
            pass

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "role": role
        })

    return Response(
        {"error": "Invalid credentials"},
        status=400
    )