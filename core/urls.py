from django.contrib import admin
from django.urls import path
from core import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginpage, name='login'),
    path('register/', views.registerpage, name='register'),
    path('logout/', views.logoutpage, name='logout'),
    path("profile/", views.profile, name="profile"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
]