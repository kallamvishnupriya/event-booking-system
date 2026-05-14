from django.urls import path
from .views import (
    get_events,
    create_event,
    update_event,
    delete_event,
    toggle_sold_out,
)

urlpatterns = [
    path('', get_events),  # ✅ /api/events/
    path('create/', create_event),  # ✅ /api/events/create/
    path('update/<int:id>/', update_event),
    path('delete/<int:id>/', delete_event),
    path('soldout/<int:id>/', toggle_sold_out),
]