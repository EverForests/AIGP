from rest_framework import serializers
from .models import ImgInfo

class ImgInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ImgInfo
        fields = '__all__'
        # read_only_fields = ('id', 'create_date')
