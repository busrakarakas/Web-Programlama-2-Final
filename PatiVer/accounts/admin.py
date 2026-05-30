from django.contrib import admin
from .models import Profil, Rozet
@admin.register(Profil)
class ProfilAdmin(admin.ModelAdmin):
    list_display=['kullanici','sosyal_bildirim']
@admin.register(Rozet)
class RozetAdmin(admin.ModelAdmin):
    list_display=['kullanici','tur','tarih']
