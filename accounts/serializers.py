from rest_framework import serializers
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from .models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password

class CustomRegisterSerializer(RegisterSerializer):
    username = None 
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})
        
        password1 = data.get("password1")
        password2 = data.get("password2")
        if password1 != password2:
            raise serializers.ValidationError({"password2": "Passwords do not match."})
        
        try:
            validate_password(password1)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({"password1": list(e.messages)})
        return data
    
    def save(self, request):
        user = super().save(request)
        role = self.validated_data.get('role')
        if role:
            user.role = role
            user.save(update_fields=['role'])
        else:
            print("Role not found in validated data")

        return user



class CustomLoginSerializer(LoginSerializer):
    username = None 
    email = serializers.EmailField(required=True)
    username_field = "email" 

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), username=email, password=password)

            if not user:
                raise serializers.ValidationError({"detail": "Unable to log in with provided credentials."})

            attrs['user'] = user
            return attrs
        else:
            raise serializers.ValidationError({"detail": "Must include \"email\" and \"password\"."})
