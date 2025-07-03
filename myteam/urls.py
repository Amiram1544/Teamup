from django.urls import path
from myteam import views

app_name = 'myteam'

urlpatterns = [

path('', views.mainpage, name='mainpage'),
path('teampage/<int:team_id>/', views.team_chat, name='team_chat'),
path("tasks/", views.taskspage , name="taskspage"),
path("add-task-ajax/", views.add_task_ajax, name="add_task_ajax"),
]
