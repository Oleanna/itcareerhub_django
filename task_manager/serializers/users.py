from typing import Any
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True
    )
    re_password = serializers.CharField(
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            're_password',
        ]

    def validate(self, attrs: dict[str, Any]) -> dict[str, Any]:
        password = attrs.get('password')
        re_password = attrs.pop('re_password')

        if password != re_password:
            raise serializers.ValidationError(
                {
                    "re_password": "Passwords must match"
                }
            )
        validate_password(password)
        return attrs

    def validate_username(self, value: str) -> str:
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def create(self, validated_data: dict[str, Any]) -> User:
        return User.objects.create_user(**validated_data)
