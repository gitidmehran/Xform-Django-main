from rest_framework import serializers
from .models import LogEntry, UploadedFile
class FileSerializer(serializers.Serializer):
    file = serializers.ListField(child=serializers.FileField())

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = '__all__'
class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = ['timestamp', 'level', 'message']  # Include the fields you want to serialize