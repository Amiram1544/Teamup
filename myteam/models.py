from django.db import models

# Create your models here.

class Teams(models.Model):
    
    #host = 
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Teams'
    
    def __str__(self):
        return self.name