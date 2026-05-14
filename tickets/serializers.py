from rest_framework import serializers
from .models import Ticket, Category
from accounts.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TicketSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.username')
    assigned_to_name = serializers.ReadOnlyField(source='assigned_to.username')
    
    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['customer', 'created_at', 'updated_at']