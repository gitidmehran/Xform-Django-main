from django.db import models
from django.contrib.auth.models import User  # Assuming you are using Django's built-in User model

class LogEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=20)
    message = models.TextField()

    def __str__(self):
        return f'{self.timestamp} - {self.level}: {self.message}'
class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploaded_files")
    upload_duration_seconds = models.FloatField(null=True, blank=True)
    user_name = models.CharField(max_length=100, null=True, blank=True, verbose_name="User Name")
    user_email = models.EmailField(null=True, blank=True, verbose_name="User Email")

    def __str__(self):
        return self.file.name
