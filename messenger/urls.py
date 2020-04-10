from django.urls import path

from . import views

app_name = "messenger"
urlpatterns = [
    path('', views.index, name='index'),
    path('rooms/', views.room, name='rooms'),
    path('rooms/<int:room_id>/', views.room, name='room'),
    path('rooms/create/<int:user_id>/', views.create_room, name='room_create'),
    path('rooms/<int:room_id>/users/<int:user_id>/', views.room_add_user, name='room_add_user'),
]
