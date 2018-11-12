from rest_framework import serializers
from . import models

class DataSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'name', 'created', 'modified', 'file',)
        model = models.Data