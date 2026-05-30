from django.urls import path
from . import views
urlpatterns = [
    path('', views.anasayfa, name='anasayfa'),
    path('giris/', views.giris_view, name='giris'),
    path('kayit/', views.kayit_view, name='kayit'),
    path('cikis/', views.cikis_view, name='cikis'),
    path('profil/', views.profil_view, name='profil'),
]
