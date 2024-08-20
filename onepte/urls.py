from django.contrib import admin
from django.urls import path
from exam.api import api
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('onepte/', api.urls),
    #URL to serve audio file
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)