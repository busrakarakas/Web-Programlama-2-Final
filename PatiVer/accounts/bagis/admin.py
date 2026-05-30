from django.contrib import admin
from .models import Kampanya,Bagis
@admin.register(Kampanya)
class KA(admin.ModelAdmin):
    list_display=['baslik','hedef','toplanan','yuzde','aktif']
    list_editable=['aktif']
@admin.register(Bagis)
class BA(admin.ModelAdmin):
    list_display=['ad_soyad','miktar','kampanya','tarih']
