from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Gonderi(models.Model):
    yazar = models.ForeignKey(User,on_delete=models.CASCADE,related_name='gonderiler')
    icerik = models.TextField(blank=True)
    resim = models.ImageField(upload_to='gonderiler/',blank=True,null=True)
    olusturuldu = models.DateTimeField(default=timezone.now)
    class Meta: ordering=['-olusturuldu']
    def __str__(self): return f'{self.yazar.username}: {self.icerik[:40]}'
    def begeni_sayisi(self): return self.begeniler.count()
    def yorum_sayisi(self): return self.yorumlar.count()
    def kullanici_begendi_mi(self,user):
        if not user.is_authenticated: return False
        return self.begeniler.filter(kullanici=user).exists()

class GonderiBegeni(models.Model):
    gonderi=models.ForeignKey(Gonderi,on_delete=models.CASCADE,related_name='begeniler')
    kullanici=models.ForeignKey(User,on_delete=models.CASCADE)
    class Meta: unique_together=('gonderi','kullanici')

class Yorum(models.Model):
    gonderi=models.ForeignKey(Gonderi,on_delete=models.CASCADE,related_name='yorumlar')
    yazar=models.ForeignKey(User,on_delete=models.CASCADE)
    metin=models.TextField()
    olusturuldu=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['olusturuldu']

class Anket(models.Model):
    gonderi=models.OneToOneField(Gonderi,on_delete=models.CASCADE,related_name='anket')
    yazar=models.ForeignKey(User,on_delete=models.CASCADE,related_name='anketler')
    soru=models.CharField(max_length=500)
    olusturuldu=models.DateTimeField(default=timezone.now)
    class Meta: ordering=['-olusturuldu']
    def __str__(self): return self.soru
    def toplam_oy(self): return sum(s.oy_sayisi for s in self.secenekler.all())
    def kullanici_oyu(self,user):
        if not user.is_authenticated: return None
        try: return AnketOy.objects.get(anket=self,kullanici=user).secenek
        except AnketOy.DoesNotExist: return None

class AnketSecenek(models.Model):
    anket=models.ForeignKey(Anket,on_delete=models.CASCADE,related_name='secenekler')
    metin=models.CharField(max_length=300)
    oy_sayisi=models.PositiveIntegerField(default=0)
    sira=models.PositiveSmallIntegerField(default=0)
    class Meta: ordering=['sira','id']
    def yuzde(self):
        t=self.anket.toplam_oy()
        return round((self.oy_sayisi/t)*100) if t else 0

class AnketOy(models.Model):
    anket=models.ForeignKey(Anket,on_delete=models.CASCADE,related_name='oylar')
    secenek=models.ForeignKey(AnketSecenek,on_delete=models.CASCADE)
    kullanici=models.ForeignKey(User,on_delete=models.CASCADE)
    tarih=models.DateTimeField(auto_now_add=True)
    class Meta: unique_together=('anket','kullanici')

class Sohbet(models.Model):
    isim=models.CharField(max_length=100)
    kanal=models.BooleanField(default=False)
    uyeler=models.ManyToManyField(User,related_name='sohbetler',blank=True)
    olusturuldu=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.isim
    def son_mesaj(self): return self.mesajlar.last()

class Mesaj(models.Model):
    sohbet=models.ForeignKey(Sohbet,on_delete=models.CASCADE,related_name='mesajlar')
    gonderen=models.ForeignKey(User,on_delete=models.CASCADE)
    metin=models.TextField()
    gonderildi=models.DateTimeField(auto_now_add=True)
    class Meta: ordering=['gonderildi']
