from django.urls import path
from . import views
urlpatterns = [
    path('', views.akis, name='akis'),
    path('gonderi/', views.gonderi_olustur, name='gonderi_olustur'),
    path('anket/', views.anket_olustur, name='anket_olustur'),
    path('oy/<int:pk>/', views.oy_ver, name='oy_ver'),
    path('begen/<int:pk>/', views.begen, name='begen'),
    path('yorum/<int:pk>/', views.yorum_ekle, name='yorum_ekle'),
    path('sohbet/', views.sohbet, name='sohbet'),
    path('sohbet/<int:pk>/mesaj/', views.mesaj_gonder, name='mesaj_gonder'),
]
