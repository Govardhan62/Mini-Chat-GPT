from django.db import models
from django.contrib.auth.models import User

class ChatHistory(models.Model):
    message = models.TextField()
    response = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
