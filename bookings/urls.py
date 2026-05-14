from django.urls import path
from .views import book_event, my_bookings

urlpatterns = [
    path("book/", book_event, name="book-event"),
    path("my/", my_bookings, name="my-bookings"),
]