from django.db import models

# Create your models here.

class Topics(models.Model):
    
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name_plural = 'Topics'
        
    def __str__(self):   
        return self.name
