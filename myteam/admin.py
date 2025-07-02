from django.contrib import admin
from .models import Teams, TeamMessages, ToDo
# Register your models here.

admin.site.register(Teams)
admin.site.register(TeamMessages)
admin.site.register(ToDo)
