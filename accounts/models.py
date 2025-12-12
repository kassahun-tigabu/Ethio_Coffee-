from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=50, blank=True)
    
    # Email verification
    email_verified = models.BooleanField(default=False)
    
    # Preferences
    newsletter_subscribed = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()