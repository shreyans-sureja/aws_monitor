from rest_framework import serializers
from .models import instance

class InstanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = instance
        fields = "__all__"

