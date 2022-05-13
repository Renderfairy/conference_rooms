from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from django.views import View

import datetime

from reservations_app.models import Room, RoomReservation

# Create your views here.


def home_page_view(request):
    return render(request, "home_page.html")


def room_list_view(request):
    rooms = Room.objects.all().order_by("capacity")
    for room in rooms:
        reservation_dates = [reservation.date for reservation in room.roomreservation_set.all()]
        room.reserved = datetime.date.today() in reservation_dates
    return render(request, "room_list.html", context={"rooms": rooms})


class AddRoom(View):
    def get(self, request):
        context = {"page_title": "Add new room"}
        return render(request, "room_form.html", context=context)

    def post(self, request):
        data = {
            "room_name": request.POST["room_name"],
            "capacity": request.POST["capacity"],
            "projector": "is_available" in request.POST,
        }
        if not data["room_name"]:
            context = {"room": data["room_name"], "page_title": "You must give a room name"}
            return render(request, "room_form.html", context=context)
        if data["capacity"] is '' or int(data["capacity"]) <= 0:
            context = {"room": data["capacity"], "page_title": "Capacity must be greather than 0"}
            return render(request, "room_form.html", context=context)
        if name != data["room_name"] and Room.objects.filter(name=data["room_name"]):
            context = {"room": data["room_name"], "page_title": "Room with that name already exists"}
            return render(request, "room_form.html", context=context)

        Room.objects.create(**data)
        return redirect(reverse("rooms_list"))


def room_detail_view(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    reservations = room.roomreservation_set.filter(date__gte=str(datetime.date.today())).order_by('date')
    context = {"room": room, "reservations": reservations}
    return render(request,"room_detail.html", context=context)


class EditRoom(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, pk=room_id)
        context = {
            "page_title": "Edit room",
            "room": room,
        }
        return render(request, "room_form.html", context=context)

    def post(self, request, room_id):
        room = get_object_or_404(Room, pk=room_id)

        room.room_name = request.POST["room_name"]
        room.capacity = request.POST["capacity"]
        room.projector = "is_available" in request.POST

        room.save()
        return redirect(reverse("rooms_list"))


class DeleteRoomView(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, pk=room_id)
        room.delete()
        return redirect(reverse("rooms_list"))


class RoomReservationView(View):
    def get(self, request, room_id):
        room = get_object_or_404(Room, id=room_id)
        return render(request, "room_reservation.html", context={"room": room})

    def post(self, request, room_id):
        room = Room.objects.get(id=room_id)
        date = request.POST.get("reservation-date")
        comment = request.POST.get("comment")

        if RoomReservation.objects.filter(room_id=room, date=date):
            return render(request, "room_reservation.html", context={
                "room": room,
                "error": "This room is already taken!"
            })

        if date < str(datetime.date.today()):
            return render(request, "room_reservation.html", context={"room": room, "error": "This date is from the past"})

        RoomReservation.objects.create(room_id=room, date=date, comment=comment)
        return redirect("rooms_list")


class SearchView(View):
    def get(self, request):
        name = request.GET.get("room-name")
        capacity = request.GET.get("capacity")
        capacity = int(capacity) if capacity else 0
        projector = request.GET.get("projector") == "on"

        rooms = Room.objects.all()
        if projector:
            rooms = rooms.filter(projector_availability=projector)
        if capacity:
            rooms = rooms.filter(capacity__gte=capacity)
        if name:
            rooms.filter(name__contains=name)

        for room in rooms:
            reservation_dates = [reservation.date for reservation in room.roomreservation_set.all()]
            room.reserved = str(datetime.date.today()) in reservation_dates

        return render(request, "room_list.html", context={"rooms": rooms, "date": datetime.date.today()})
