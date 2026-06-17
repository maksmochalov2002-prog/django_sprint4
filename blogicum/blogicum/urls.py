from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from pages.views import page_not_found, server_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('django.contrib.auth.urls')),
    path('', include('blog.urls')),
    path('pages/', include('pages.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = page_not_found
handler500 = server_error