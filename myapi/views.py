import logging
import os
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import LogEntry, UploadedFile
from drk.authentication import KeyCloakAuthentication
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from .process_file import process_file
from drk import settings
from .serializers import LogEntrySerializer
# from rest_framework.decorators import api_view


class FileUploadView(APIView):
    authentication_classes = [KeyCloakAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        user_info = request.user.user_info
        user_email = user_info.get('email', '')
        user, created = User.objects.get_or_create(
            username=user_info['preferred_username'],
            defaults={'email': user_email, 'first_name': user_info['given_name'], 'last_name': user_info['family_name']})
        start_time = datetime.now()
        selected_database = request.data.get('database', 'Dev')
        files = request.FILES.getlist('file')
        uploaded_files = []
        failed_files = []  # List to store names of failed files
        upload_dir = 'uploads/'
        os.makedirs(os.path.join(settings.MEDIA_ROOT,
                    upload_dir), exist_ok=True)
        for uploaded_file in files:
            filename = uploaded_file.name
            file_path = os.path.join(settings.MEDIA_ROOT, upload_dir, filename)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            file_instance = UploadedFile(
                file=upload_dir + filename,
                uploaded_by=user,
                user_name=user_info.get('name', ''),
                user_email=user_info.get('email', ''),
            )
            file_instance.save()
            uploaded_files.append(file_instance.file.url)
            file_url = request.build_absolute_uri(
                "/media/" + file_instance.file.name)
            start_processing_time = timezone.now()
            xls = process_file(file_url, 'db', selected_database, filename)
            if not xls:
                # Add the filename to the list of failed files
                failed_files.append(filename)
        # Send email after processing all files
        recipient_list = [
            user_email, 'zia.iqbal@researchquran.org', 'wajid.ahmad@vitalanalytics.net']
        if failed_files:
            # Extract filenames from URLs for successful and failed files
            successful_filenames = [os.path.basename(
                url) for url in uploaded_files]
            failed_filenames = [os.path.basename(url) for url in failed_files]
            send_mail(
                'File Upload Failed',
                f'Upload failed: The following files were uploaded by "{user_info.get("name", "")}" in database {selected_database}: Successful files: {
                    ", ".join(successful_filenames)}. However, the following files failed to upload: {", ".join(failed_filenames)}.',
                'admin@researchquran.org',
                recipient_list,
                fail_silently=False
            )
            return JsonResponse({
                'message': 'Files uploaded with failures',
                'file_urls': uploaded_files,
                'failed_files': failed_files,
            }, status=status.HTTP_206_PARTIAL_CONTENT)
        else:
            # Extract filenames from URLs for successful files
            successful_filenames = [os.path.basename(
                url) for url in uploaded_files]
            send_mail(
                'File Upload Completed',
                f'All files were uploaded successfully by "{user_info.get("name", "")}" in database {
                    selected_database}. Successful files: {", ".join(successful_filenames)}.',
                'admin@researchquran.org',
                recipient_list,
                fail_silently=False
            )
            return JsonResponse({
                'message': 'Files uploaded successfully',
                'file_urls': uploaded_files,
            }, status=status.HTTP_201_CREATED)

        # If no files were processed, return an error response
        return JsonResponse({
            'message': 'No files were processed',
            'file_urls': uploaded_files,
            'failed_files': failed_files,
        }, status=status.HTTP_400_BAD_REQUEST)
# @api_view(['DELETE'])


class UploadedFileDelete(APIView):
    authentication_classes = [KeyCloakAuthentication]

    def delete(self, request, pk, format=None):
        try:
            uploaded_file = UploadedFile.objects.get(pk=pk)
            uploaded_file.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UploadedFile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
# @api_view(['GET'])


class UploadedFileListView(APIView):
    authentication_classes = [KeyCloakAuthentication]

    def get(self, request):
        # Query the database to retrieve all UploadedFile objects
        uploaded_files = UploadedFile.objects.all()
        data = [{"file": file.file.url, "id": file.id, "uploaded_at": file.uploaded_at, "uploaded_by": file.uploaded_by.username,
                 "upload_duration_seconds": file.upload_duration_seconds} for file in uploaded_files]
        return Response(data)


class LogEntryListView(APIView):
    authentication_classes = [KeyCloakAuthentication]

    def get(self, request):
        # Query the database to retrieve all LogEntry objects
        log_entries = LogEntry.objects.all()
        serializer = LogEntrySerializer(
            log_entries, many=True)  # Serialize the queryset
        return Response(serializer.data)


class FileUploadViewUpdate(APIView):
    authentication_classes = [KeyCloakAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        user_info = request.user.user_info
        user_email = user_info.get('email', '')
        user, created = User.objects.get_or_create(
            username=user_info['preferred_username'],
            defaults={'email': user_email, 'first_name': user_info['given_name'], 'last_name': user_info['family_name']})
        start_time = datetime.now()
        selected_database = request.data.get('database', 'Dev')
        files = request.FILES.getlist('file')
        confirm = request.data.get('selectTF')
        uploaded_files = []
        failed_files = []  # List to store names of failed files
        upload_dir = 'uploads/'
        os.makedirs(os.path.join(settings.MEDIA_ROOT,
                    upload_dir), exist_ok=True)
        for uploaded_file in files:
            filename = uploaded_file.name
            file_path = os.path.join(settings.MEDIA_ROOT, upload_dir, filename)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            file_instance = UploadedFile(
                file=upload_dir + filename,
                uploaded_by=user,
                user_name=user_info.get('name', ''),
                user_email=user_info.get('email', ''),
            )
            file_instance.save()
            uploaded_files.append(file_instance.file.url)
            file_url = request.build_absolute_uri(
                "/media/" + file_instance.file.name)
            start_processing_time = timezone.now()
            xls = process_file(file_url, 'db', selected_database, filename,confirm)
            if not xls:
                # Add the filename to the list of failed files
                failed_files.append(filename)
        # Send email after processing all files
        recipient_list = [
            user_email, 'zia.iqbal@researchquran.org', 'wajid.ahmad@vitalanalytics.net']
        if failed_files:
            # Extract filenames from URLs for successful and failed files
            successful_filenames = [os.path.basename(
                url) for url in uploaded_files]
            failed_filenames = [os.path.basename(url) for url in failed_files]
            send_mail(
                'File Upload Failed',
                f'Upload failed: The following files were uploaded by "{user_info.get("name", "")}" in database {selected_database}: Successful files: {
                    ", ".join(successful_filenames)}. However, the following files failed to upload: {", ".join(failed_filenames)}.',
                'admin@researchquran.org',
                recipient_list,
                fail_silently=False
            )
            return JsonResponse({
                'message': 'Files uploaded with failures',
                'file_urls': uploaded_files,
                'failed_files': failed_files,
            }, status=status.HTTP_206_PARTIAL_CONTENT)
        else:
            # Extract filenames from URLs for successful files
            successful_filenames = [os.path.basename(
                url) for url in uploaded_files]
            send_mail(
                'File Upload Completed',
                f'All files were uploaded successfully by "{user_info.get("name", "")}" in database {
                    selected_database}. Successful files: {", ".join(successful_filenames)}.',
                'admin@researchquran.org',
                recipient_list,
                fail_silently=False
            )
            return JsonResponse({
                'message': 'Files uploaded successfully',
                'file_urls': uploaded_files,
            }, status=status.HTTP_201_CREATED)

        # If no files were processed, return an error response
        return JsonResponse({
            'message': 'No files were processed',
            'file_urls': uploaded_files,
            'failed_files': failed_files,
        }, status=status.HTTP_400_BAD_REQUEST)