from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profil(models.Model):
    kullanici = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatarlar/', blank=True, null=True)
    sosyal_bildirim = models.BooleanField(default=True)
    etkinlik_bildirim = models.BooleanField(default=False)

    def __str__(self): return f'{self.kullanici.username} profili'
    def harf(self):
        ad = self.kullanici.get_full_name()
        return (ad[0] if ad else self.kullanici.username[0]).upper()
    def rozet_listesi(self):
        k = set(self.kullanici.rozetler.values_list('tur',flat=True))
        tum=[
            {'key':'ilk_dost','isim':'İlk Dost','emoji':'🐾','aciklama':'İlk hayvanınızı sahiplendiniz.'},
            {'key':'comert_pati','isim':'Cömert Pati','emoji':'💎','aciklama':'İlk bağışınızı yaptınız.'},
            {'key':'kayip_avci','isim':'Kayıp Avcısı','emoji':'🔍','aciklama':'Bir kayıp ilanı oluşturdunuz.'},
            {'key':'kahraman','isim':'Topluluk Kahramanı','emoji':'👑','aciklama':'Topluluğa büyük katkı sağladınız.'},
        ]
        for r in tum: r['kazanildi']=r['key'] in k
        return tum

class Rozet(models.Model):
    TURLER=[('ilk_dost','İlk Dost'),('comert_pati','Cömert Pati'),('kayip_avci','Kayıp Avcısı'),('kahraman','Kahraman')]
    kullanici = models.ForeignKey(User,on_delete=models.CASCADE,related_name='rozetler')
    tur = models.CharField(max_length=30,choices=TURLER)
    tarih = models.DateTimeField(auto_now_add=True)
    class Meta: unique_together=('kullanici','tur')

@receiver(post_save,sender=User)
def profil_olustur(sender,instance,created,**kwargs):
    if created: Profil.objects.get_or_create(kullanici=instance)
