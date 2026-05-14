from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):

    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()

    # 👑 organizer/manager creator
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    # 🔥 SOLD OUT FIELD (manual override by manager)
    is_sold_out = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    # 🔥 ACTUAL SOLD OUT LOGIC (important)
    @property
    def is_full(self):
        return self.booking_set.count() >= self.capacity