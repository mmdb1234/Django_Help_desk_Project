# chats/views.py
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from tickets.models import Ticket

class ChatMessageViewSet(viewsets.ModelViewSet):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = ChatMessage.objects.all().order_by('-created_at')

    def get_queryset(self):
        user = self.request.user
        ticket_id = self.request.query_params.get('ticket')
        
        if ticket_id:
            try:
                ticket = Ticket.objects.get(id=ticket_id)
                if user.role in ['admin', 'support'] or ticket.customer == user:
                    return ChatMessage.objects.filter(ticket_id=ticket_id)
            except Ticket.DoesNotExist:
                pass
            return ChatMessage.objects.none()
        
        if user.role in ['admin', 'support']:
            return ChatMessage.objects.all()
        
        return ChatMessage.objects.filter(ticket__customer=user)
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
    
    @action(detail=False, methods=['post'])
    def mark_as_read(self, request):
        """علامت‌گذاری پیام‌ها به عنوان خوانده شده"""
        ticket_id = request.data.get('ticket_id')
        user = request.user
        
        messages = ChatMessage.objects.filter(
            ticket_id=ticket_id,
            is_read=False
        ).exclude(sender=user)
        
        count = messages.update(is_read=True)
        return Response({'marked_as_read': count})