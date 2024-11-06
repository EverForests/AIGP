from rest_framework import serializers
from .models import CUser

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CUser
        fields = ['username', 'password']
        read_only_fields = ('id', 'create_date')