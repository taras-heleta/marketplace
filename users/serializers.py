from rest_framework import serializers
from .models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id', 
            'email', 
            'first_name', 
            'last_name', 
            'phone_number',
            'avatar',
            'role',
            'is_active',
            'created_at',
            'updated_at',
            'password'
        )
        read_only_fields = ('id', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # username = email, because we use email for login, it's by default for simplejwt 
        validated_data['username'] = validated_data.get('email')
        validated_data['password'] = make_password(validated_data.get('password'))
        
        return super().create(validated_data)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )
            if not user:
                raise serializers.ValidationError('Unable to log in with provided credentials.')
            
            if not user.is_active:
                raise serializers.ValidationError('User account is disabled.')

            refresh = self.get_token(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
            return data
        else:
            raise serializers.ValidationError('Must include "email" and "password".')

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer