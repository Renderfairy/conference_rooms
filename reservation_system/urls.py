"""reservation_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from reservations_app.views import(
    home_page_view,
    room_list_view,
    AddRoom,
    room_detail_view,
    EditRoom,
    DeleteRoomView,
    RoomReservationView,
    SearchView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page_view, name='home_page'),
    path('room-list/', room_list_view, name='rooms_list'),
    path('room-new/', AddRoom.as_view(), name='room_add'),
    path('room-details/<int:room_id>/', room_detail_view, name='room_detail'),
    path('room-modify/<int:room_id>/', EditRoom.as_view(), name='room_edit'),
    path('room-del/<int:room_id>/', DeleteRoomView.as_view(), name='room_delete'),
    path('room-reservation/<int:room_id>', RoomReservationView.as_view(), name='room_reservation'),
    path('search/', SearchView.as_view(), name="room_search"),
]
