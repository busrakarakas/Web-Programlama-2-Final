from django.db import models
from django.contrib.auth.models import User

class Veteriner(models.Model):
    isim=models.CharField(max_length=200)
    adres=models.CharField(max_length=300)
    telefon=models.CharField(max_length=20)
    email=models.EmailField()
    uzmanlik=models.CharField(max_length=100,default='Genel Veterinerlik')
    puan=models.DecimalField(max_digits=3,decimal_places=1,default=4.8)
    aktif=models.BooleanField(default=True)
    class Meta: verbose_name='Veteriner'
    def __str__(self): return self.isim

class Randevu(models.Model):
    DURUM=[('bekliyor','Bekliyor'),('onaylandi','Onaylandı'),('iptal','İptal')]
    veteriner=models.ForeignKey(Veteriner,on_delete=models.CASCADE,related_name='randevular')
    kullanici=models.ForeignKey(User,on_delete=models.CASCADE,related_name='randevular')
    hayvan_adi=models.CharField(max_length=100)
    sahip_adi=models.CharField(max_length=100)
    telefon=models.CharField(max_length=20)
    tarih=models.DateField()
    neden=models.TextField()
    durum=models.CharField(max_length=20,choices=DURUM,default='bekliyor')
    olusturuldu=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['-olusturuldu']
    def __str__(self): return f'{self.hayvan_adi} — {self.veteriner.isim}'
