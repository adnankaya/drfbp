from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from django.db import transaction
from django.contrib.auth import get_user_model
from django.utils.translation import gettext as _

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = (
            "id", "email", "username", "password", "password2",
            "first_name", "last_name", "phone", "email_verified",

        )
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5},
            "email_verified": {"read_only": True},
        }

    def create(self, validated_data):
        password2 = validated_data.pop("password2")
        if validated_data.get("password") != password2:
            raise ValidationError(_("Passwords did not match!"))
        try:
            with transaction.atomic():
                user = User.objects.create_user(**validated_data)

                return user
        except Exception as e:
            raise e


class UserUpdateSerializer(UserSerializer):
    class Meta(UserSerializer.Meta):
        fields = (
            "id", "email", "first_name", "last_name",
            "phone", "username",
        )


class UserCreateSerializer(UserSerializer):
    pass


class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField()
    password2 = serializers.CharField()
    old_password = serializers.CharField()

    def validate(self, attrs):
        user = self.context["request"].user
        if not user.check_password(attrs["old_password"]):
            raise ValidationError(_("password is wrong"))
        if not attrs["password"] == attrs["password2"]:
            raise ValidationError(_("password and password2 do not match"))
        return super().validate(attrs)
