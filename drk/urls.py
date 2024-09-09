from django.contrib import admin
from django.urls import path, include
from drk import settings 
from django.conf.urls.static import static
from drk.views import SampleResource

urlpatterns = [
    path("admin/", admin.site.urls),
    path(r"", SampleResource.as_view({"get": "list"})),
    path('api/', include('myapi.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    