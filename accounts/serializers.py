
from rest_framework import serializers

from accounts.helpers import send_otp_to_mobile
from .models import *
from .helpers import *

# from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    # User = get_user_model()

    class Meta:
        model = User
        fields = ['email', 'phone', 'password']

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'], phone=validated_data['phone'])
        user.set_password(validated_data['password'])
        send_otp_to_mobile(user.phone, user)

        user.save()
        return user
