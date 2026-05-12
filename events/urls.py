from django.urls import path

from .views import (
    get_events,
    create_event,
    update_event,
    delete_event,
    toggle_sold_out,
)

urlpatterns = [
    path('events/', get_events),

    path('events/create/', create_event),

    path('events/update/<int:id>/', update_event),

    path('events/delete/<int:id>/', delete_event),

    path('events/soldout/<int:id>/', toggle_sold_out),
]