from django.urls import path
from myteam import views

app_name = 'myteam'

urlpatterns = [

path('', views.mainpage, name='mainpage'),

]
