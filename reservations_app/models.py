from django.db import models

# Create your models here.

# Dodaj model reprezentujący salę. Powinien przechowywać takie informacje, jak:
# nazwa sali (pole tekstowe, maks 255 znaków, unikatowe),
# pojemność sali (pole typu liczbowego całkowitego),
# dostępność rzutnika (pole typu boolean).


class Room(models.Model):
    room_name = models.CharField(max_length=255)
    capacity = models.PositiveSmallIntegerField()
    projector = models.BooleanField(default=True)


class RoomReservation(models.Model):
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ('room_id', 'date',)
