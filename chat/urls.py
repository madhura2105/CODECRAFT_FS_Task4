from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path("login/", views.login_page, name="login"),
    path("rooms/", views.rooms, name="rooms"),
    path("room/<str:room_name>/", views.room_chat, name="room_chat"),
]