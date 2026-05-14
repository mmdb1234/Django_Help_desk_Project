# accounts/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .serializers import UserSerializer, RegisterSerializer
from .permissions import IsSupportOrAdmin, IsAdmin

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'register':
            return [AllowAny()]
        elif self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]  
        elif self.action == 'list':
            return [IsSupportOrAdmin()] 
        else:
            return [IsAuthenticated()]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        if 'role' in request.data:
            return Response(
                {'error': 'شما نمی‌توانید نقش انتخاب کنید. نقش به طور خودکار مشتری تعیین می‌شود.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  
            refresh = RefreshToken.for_user(user)
            return Response({
                'user': UserSerializer(user).data,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'message': 'ثبت نام با موفقیت انجام شد. نقش شما: مشتری'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAdmin])
    def change_role(self, request, pk=None):
        """فقط ادمین می‌تواند نقش کاربر را تغییر دهد"""
        user = self.get_object()
        new_role = request.data.get('role')
        
        if new_role not in ['customer', 'support', 'admin']:
            return Response(
                {'error': 'نقش نامعتبر است. نقش‌های مجاز: customer, support, admin'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        old_role = user.role
        user.role = new_role
        user.save()
        
        return Response({
            'message': f'نقش کاربر {user.username} از {old_role} به {new_role} تغییر کرد',
            'user': UserSerializer(user).data
        })