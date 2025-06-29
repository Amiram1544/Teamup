from django.urls import path
from chatrooms import views

app_name = 'chatrooms'

urlpatterns = [
    path('room/<int:pk>/', views.room, name='room'),
]
