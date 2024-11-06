from rest_framework import serializers
from .models import Follow

class UserRelationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = '__all__'
        read_only_fields = ['id']
