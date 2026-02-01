from rest_framework import serializers

from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "email", "username"]


class LoginUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "password"]

    def validate(self, attrs):
        user = authenticate(email=attrs["email"], password=attrs["password"])

        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credenciales incorrectas, correo o contraseña no coinciden.")



class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, validators=[validate_password])

    class Meta:
        model = CustomUser
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            username=validated_data["username"],
            password=validated_data["password"]
        )
        return user

    