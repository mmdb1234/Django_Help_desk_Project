from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'phone', 'avatar']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'phone']
    
    def validate(self, data):
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "این نام کاربری قبلاً ثبت شده است"})
        
        # بررسی اینکه ایمیل تکراری نباشد
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "این ایمیل قبلاً ثبت شده است"})
        
        return data
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            phone=validated_data.get('phone', ''),
            role='customer'  
        )
        return user