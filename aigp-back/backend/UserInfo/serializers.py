from rest_framework import serializers
from .models import UInfo

class UserInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = UInfo
        fields = '__all__'
        # read_only_fields = ('id')
