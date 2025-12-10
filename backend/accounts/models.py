from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=50, blank=True)
    region = models.CharField(max_length=50, blank=True)
    
    # Email verification
    email_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    
    # Preferences
    newsletter_subscribed = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email