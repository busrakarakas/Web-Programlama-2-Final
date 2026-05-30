from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'accounts.views.hata_404'
handler500 = 'accounts.views.hata_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('sosyal/', include('sosyal.urls')),
    path('bagis/', include('bagis.urls')),
    path('veteriner/', include('veteriner.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
