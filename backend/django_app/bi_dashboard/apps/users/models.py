from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Organization(models.Model):
    name = models.CharField(max_length=255)
    members = models.ManyToManyField(
        User, 
        related_name='organizations'
        )

    def __str__(self):
        return self.name
    
