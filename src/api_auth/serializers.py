from django.contrib import auth
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth.get_user_model()
        fields = ("email", "password")
        extra_kwargs = {
            "password": {
                "write_only": True,
            }
        }

    def validate(self, attrs: dict):
        password = attrs.get("password")

        validate_password(password)

        return super().validate(attrs)

    def create(self, validated_data: dict):
        email = validated_data.get("email")
        password = validated_data.get("password")
        user = self.Meta.model.objects.create_user(email, password)

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True, style={"input_type": "password"})

    def validate(self, attrs: dict):
        email = attrs.get("email")
        password = attrs.get("password")
        user = auth.authenticate(self.context.get("request"), email=email, password=password)

        if not user:
            raise serializers.ValidationError("Access denied: wrong email or password", "authorization")

        attrs["user"] = user

        return super().validate(attrs)
