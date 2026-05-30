from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal

class Kampanya(models.Model):
    baslik=models.CharField(max_length=200)
    aciklama=models.TextField()
    hedef=models.DecimalField(max_digits=10,decimal_places=2)
    toplanan=models.DecimalField(max_digits=10,decimal_places=2,default=Decimal('0'))
    emoji=models.CharField(max_length=10,default='❤️')
    aktif=models.BooleanField(default=True)
    olusturuldu=models.DateTimeField(default=timezone.now)
    class Meta: ordering=['-olusturuldu']
    def __str__(self): return self.baslik
    def yuzde(self): return min(100,round(float(self.toplanan)/float(self.hedef)*100)) if self.hedef else 0

class Bagis(models.Model):
    kullanici=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True,related_name='bagislar')
    kampanya=models.ForeignKey(Kampanya,on_delete=models.SET_NULL,null=True,blank=True,related_name='bagislar')
    miktar=models.DecimalField(max_digits=10,decimal_places=2)
    ad_soyad=models.CharField(max_length=100,blank=True,default='Anonim')
    tarih=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-tarih']
    def __str__(self): return f'{self.ad_soyad} — {self.miktar}₺'
