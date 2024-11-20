from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import base
import assignment
import accounts
import lecture
import thread

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('assignment/', include('assignment.urls')),
    path('accounts/', include('accounts.urls')),
    path('lecture/', include('lecture.urls')),
    path('thread/', include('thread.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)