from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('coach', 'Coach'),
        ('agent', 'Agent'),
        ('player', 'Football Player'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, blank=False)
    email = models.EmailField(unique=True)  
    username = None  

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} - {self.role}"
