from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Ticket, Category
from .serializers import TicketSerializer, CategorySerializer

class IsSupportOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['support', 'admin']

class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().order_by('-created_at')
    serializer_class = TicketSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'category']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'priority']
    
    def get_queryset(self):
        user = self.request.user
        if user.role == 'customer':
            return Ticket.objects.filter(customer=user)
        return Ticket.objects.all()  # support و admin همه را می‌بینند
    
    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]