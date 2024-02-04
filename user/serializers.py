from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "is_superuser", "is_staff", "is_active", "date_joined", "last_login"]


class UserPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["last_login", "date_joined", "is_superuser", "is_staff"]


class UserPatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "last_login", "date_joined", "is_superuser", "is_staff", "is_active"]
