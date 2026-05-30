from django.contrib import admin
from .models import Veteriner,Randevu
@admin.register(Veteriner)
class VA(admin.ModelAdmin):
    list_display=['isim','telefon','uzmanlik','puan','aktif']
    list_editable=['aktif']
@admin.register(Randevu)
class RA(admin.ModelAdmin):
    list_display=['hayvan_adi','sahip_adi','veteriner','tarih','durum']
    list_editable=['durum']
    list_filter=['durum','veteriner']
