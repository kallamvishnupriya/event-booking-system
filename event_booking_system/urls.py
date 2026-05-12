from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

urlpatterns = [

    path('admin/', admin.site.urls),

    # apps
    path('api/', include('users.urls')),
    path('api/', include('events.urls')),
    path('api/', include('bookings.urls')),

    # jwt refresh only
    path(
        'api/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
]