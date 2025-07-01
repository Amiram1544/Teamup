from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Teams(models.Model):
    
    host = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1, related_name='team_host')
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='team_members')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Teams'
    
    def __str__(self):
        return self.name
    
class TeamMessages(models.Model):
    
    team = models.ForeignKey(Teams, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Team_Messages'
        ordering = ['-created']
        
    def __str__(self):
        return self.body[0:50]