from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone
from datetime import timedelta

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
    members = models.ManyToManyField(User, related_name='teams')
    body = models.TextField()
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Team_Messages'
        ordering = ['-created']
        
    def __str__(self):
        return self.body[0:50]
    
class ToDo(models.Model):
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = 'Tasks'
        ordering = ['-created']
        
    def __str__(self):
        return self.topic
    
class TeamTasks(models.Model):
    
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    assinged_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="assigned_tasks", blank=True)
    topic = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    
    def time_left(self):
        
        if self.deadline:
            delta = self.deadline - timezone.now()
            if delta.total_seconds() <= 0:
                return 'Deadline is over'
            else:
                days = delta.days
                hours = delta.seconds // 3600
                minutes = (delta.seconds%3600) // 60
                
                return f'{days} days & {hours} hours {minutes} minutes.'
            
        return 'no deadline' 
        
    class Meta:
        verbose_name_plural = 'Team Tasks'
        ordering = ['-created']
        
    def __str__(self):
        return self.topic[0:50]
    
    
class Feed(models.Model):
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    subject = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    seen = models.BooleanField(default=False)
    team = models.ForeignKey(Teams, on_delete=models.CASCADE, null=True, blank=True)
    sender_user = models.ForeignKey(User, related_name='direct_sender', on_delete=models.CASCADE, null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
        
    def __str__(self):
        return f"{self.user.username}: {self.subject}"
    
    
class Directs(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_directs", null=True, blank=True )
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_directs", null=True, blank=True)
    parent = models.ForeignKey('self',null=True, blank=True, on_delete=models.SET_NULL)
    body = models.TextField()
    timesent = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)
    
    class Meta:
        verbose_name_plural = "Directs"
        ordering = ["timesent"]
        
    def __str__(self):
        return self.body[:50]