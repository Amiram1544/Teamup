from django.urls import path
from myteam import views

app_name = 'myteam'

urlpatterns = [

path('', views.mainpage, name='mainpage'),
path('teampage/<int:team_id>/', views.team_chat, name='team_chat'),
path("tasks/", views.taskspage , name="taskspage"),
path("add-task-ajax/", views.add_task_ajax, name="add_task_ajax"),
path('complete-task-ajax/', views.complete_task_ajax, name='complete-task-ajax'),
path('delete-task-ajax/', views.delete_task_ajax, name='delete-task-ajax'),
path('news/', views.news, name='news'),
path("team-task/<int:team_id>/", views.team_task, name="team_task"),
path("get-user-tasks/", views.get_user_tasks, name='get-user-tasks'),
path("direct-messages/", views.pv, name='inbox'),
path("direct-messages/<str:username>/", views.pv, name='pv-view'),
path("myteam/unseen_count/", views.get_unseen, name='unseen-count'),
path("delete-notif/", views.delete_notif, name='delete-notif'),
]
