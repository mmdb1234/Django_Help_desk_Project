# chats/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from tickets.models import Ticket
from .models import ChatMessage
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        self.room_group_name = f'chat_{self.ticket_id}'
        
        query_string = self.scope['query_string'].decode()
        token = None
        for param in query_string.split('&'):
            if param.startswith('token='):
                token = param.split('=')[1]
                break
        
        user = await self.get_user_from_token(token)
        
        if not user or user.is_anonymous:
            await self.close(code=4001)
            return
        
        self.scope['user'] = user
        
        has_access = await self.check_user_access(user, self.ticket_id)
        
        if not has_access:
            await self.close(code=4003)  # 403 Forbidden
            return
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        print(f"✅ WebSocket connected: User {user.username} to ticket {self.ticket_id}")
    
    async def disconnect(self, close_code):
        print(f"🔌 WebSocket disconnected: {close_code}")
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type', 'message')
        user = self.scope['user']
        
        if message_type == 'message':
            message = text_data_json.get('message', '')
            
            if not message:
                return
            
            saved_message = await self.save_message(
                ticket_id=self.ticket_id,
                sender=user,
                message=message
            )
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': user.username,
                    'user_id': user.id,
                    'user_role': user.role,
                    'created_at': saved_message['created_at'],
                    'message_id': saved_message['id']
                }
            )
        
        elif message_type == 'status_update':
            new_status = text_data_json.get('status')
            
            if user.role in ['admin', 'support'] and new_status:
                await self.update_ticket_status(self.ticket_id, new_status)
                
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'status_update',
                        'status': new_status,
                        'updated_by': user.username,
                        'updated_by_role': user.role
                    }
                )
    
    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event['message'],
            'username': event['username'],
            'user_id': event['user_id'],
            'user_role': event.get('user_role', ''),
            'created_at': event['created_at'],
            'message_id': event.get('message_id')
        }))
    
    async def status_update(self, event):
        await self.send(text_data=json.dumps({
            'type': 'status_update',
            'status': event['status'],
            'updated_by': event['updated_by'],
            'updated_by_role': event.get('updated_by_role', '')
        }))
    
    @database_sync_to_async
    def get_user_from_token(self, token):
        """دریافت کاربر از توکن JWT"""
        try:
            if not token:
                return AnonymousUser()
            
            access_token = AccessToken(token)
            user_id = access_token['user_id']
            user = User.objects.get(id=user_id)
            return user
        except Exception as e:
            print(f"Token validation error: {e}")
            return AnonymousUser()
    
    @database_sync_to_async
    def check_user_access(self, user, ticket_id):
        """بررسی دسترسی کاربر به تیکت"""
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            
            if user.role in ['admin', 'support']:
                return True
            
            if user.role == 'customer':
                return ticket.customer == user
            
            return False
        except Ticket.DoesNotExist:
            return False
    
    @database_sync_to_async
    def save_message(self, ticket_id, sender, message):
        """ذخیره پیام در دیتابیس"""
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            chat_message = ChatMessage.objects.create(
                ticket=ticket,
                sender=sender,
                message=message
            )
            return {
                'id': chat_message.id,
                'created_at': chat_message.created_at.isoformat()
            }
        except Exception as e:
            print(f"Save message error: {e}")
            return {'id': None, 'created_at': None}
    
    @database_sync_to_async
    def update_ticket_status(self, ticket_id, new_status):
        """به‌روزرسانی وضعیت تیکت"""
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            ticket.status = new_status
            ticket.save()
            return ticket.status
        except Exception as e:
            print(f"Update status error: {e}")
            return None