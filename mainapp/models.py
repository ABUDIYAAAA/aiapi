from django.db import models

# Create your models here.


class ChatSession(models.Model):
    session_id = models.CharField(max_length=255, unique=True)
    messages = models.JSONField(
        default=list
    )  # Stores the conversation as a list of messages
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
