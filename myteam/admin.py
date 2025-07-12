from django.contrib import admin
from .models import Teams, TeamMessages, ToDo, TeamTasks, Directs
# Register your models here.

admin.site.register(Teams)
admin.site.register(TeamMessages)
admin.site.register(TeamTasks)
admin.site.register(ToDo)
admin.site.register(Directs)
