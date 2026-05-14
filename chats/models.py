# chats/models.py
from django.db import models
from django.conf import settings
from tickets.models import Ticket

class ChatMessage(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['created_at']
        verbose_name = 'پیام چت'
        verbose_name_plural = 'پیام‌های چت'
    
    def __str__(self):
        return f"{self.sender.username}: {self.message[:50]}"