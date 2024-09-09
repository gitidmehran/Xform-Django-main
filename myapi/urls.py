from django import views
from django.conf import settings
from django.urls import path
from .views import FileUploadView, FileUploadViewUpdate, LogEntryListView,UploadedFileListView,UploadedFileDelete

urlpatterns = [
    path('files', FileUploadView.as_view(), name='file-upload'),
    path('files/update', FileUploadViewUpdate.as_view(), name='file-update'),
    path('uploaded-files', UploadedFileListView.as_view(), name='uploaded-files-list'),
    path('delete/<int:pk>', UploadedFileDelete.as_view(), name='uploadedfile-delete'),
    path('log-entries', LogEntryListView.as_view(), name='log_entries_api'),
]
