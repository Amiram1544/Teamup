from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Topics(models.Model):
    
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = 'Topics'
        
    def __str__(self):   
        return self.name
    
class Rooms(models.Model):
    
    topics = models.ForeignKey(Topics, verbose_name=("topic"), on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, blank=True, related_name='participants')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Rooms'
        ordering = ['-updated', '-created']
        
    def __str__(self):
        return self.name