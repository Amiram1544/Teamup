from django.db import models
from core.models import Rooms
from django.contrib.auth.models import User

# Create your models here.

class Messages(models.Model):
    
    rooms = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated =  models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.body[0:50]