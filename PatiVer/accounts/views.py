from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum
from django import forms as f
from .models import Profil

class GirisForm(f.Form):
    username = f.CharField(label='Kullanıcı Adı', widget=f.TextInput(attrs={'class':'form-input','placeholder':'kullanici_adi','autofocus':True}))
    password = f.CharField(label='Şifre', widget=f.PasswordInput(attrs={'class':'form-input','placeholder':'••••••••'}))

class KayitForm(f.Form):
    first_name = f.CharField(label='Ad',max_length=50,widget=f.TextInput(attrs={'class':'form-input','placeholder':'Adınız'}))
    last_name  = f.CharField(label='Soyad',max_length=50,widget=f.TextInput(attrs={'class':'form-input','placeholder':'Soyadınız'}))
    username   = f.CharField(label='Kullanıcı Adı',max_length=30,widget=f.TextInput(attrs={'class':'form-input','placeholder':'kullanici_adi'}))
    email      = f.EmailField(label='E-posta',widget=f.EmailInput(attrs={'class':'form-input','placeholder':'ornek@email.com'}))
    password   = f.CharField(label='Şifre',min_length=6,widget=f.PasswordInput(attrs={'class':'form-input','placeholder':'En az 6 karakter'}))
    password2  = f.CharField(label='Şifre Tekrar',widget=f.PasswordInput(attrs={'class':'form-input','placeholder':'Şifreyi tekrar girin'}))
    def clean_username(self):
        un=self.cleaned_data['username']
        if User.objects.filter(username=un).exists(): raise f.ValidationError('Bu kullanıcı adı alınmış.')
        return un
    def clean_email(self):
        em=self.cleaned_data['email']
        if User.objects.filter(email=em).exists(): raise f.ValidationError('Bu e-posta zaten kayıtlı.')
        return em
    def clean(self):
        cd=super().clean()
        if cd.get('password')!=cd.get('password2'): raise f.ValidationError('Şifreler eşleşmiyor.')
        return cd

def anasayfa(request):
    from sosyal.models import Gonderi
    from bagis.models import Kampanya
    return render(request,'anasayfa.html',{
        'son_gonderiler':Gonderi.objects.select_related('yazar').order_by('-olusturuldu')[:3],
        'kampanyalar':Kampanya.objects.filter(aktif=True)[:4],
    })

def giris_view(request):
    if request.user.is_authenticated: return redirect('anasayfa')
    form=GirisForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        user=authenticate(request,username=form.cleaned_data['username'],password=form.cleaned_data['password'])
        if user:
            login(request,user)
            messages.success(request,f'Hoş geldin, {user.get_full_name() or user.username}! 🐾')
            return redirect(request.GET.get('next','anasayfa'))
        messages.error(request,'Kullanıcı adı veya şifre hatalı.')
    return render(request,'accounts/giris.html',{'form':form})

def kayit_view(request):
    if request.user.is_authenticated: return redirect('anasayfa')
    form=KayitForm(request.POST or None)
    if request.method=='POST' and form.is_valid():
        cd=form.cleaned_data
        user=User.objects.create_user(username=cd['username'],email=cd['email'],password=cd['password'],first_name=cd['first_name'],last_name=cd['last_name'])
        login(request,user)
        messages.success(request,'Hoş geldin! PatiVer ailesine katıldın 🎉')
        return redirect('anasayfa')
    return render(request,'accounts/kayit.html',{'form':form})

def cikis_view(request):
    logout(request)
    messages.info(request,'Çıkış yapıldı. Görüşürüz! 👋')
    return redirect('anasayfa')

@login_required
def profil_view(request):
    profil,_=Profil.objects.get_or_create(kullanici=request.user)
    from bagis.models import Bagis
    from sosyal.models import Gonderi
    toplam_bagis=Bagis.objects.filter(kullanici=request.user).aggregate(t=Sum('miktar'))['t'] or 0
    gonderi_sayisi=Gonderi.objects.filter(yazar=request.user).count()
    if request.method=='POST':
        request.user.first_name=request.POST.get('first_name','').strip()
        request.user.last_name=request.POST.get('last_name','').strip()
        request.user.save()
        profil.bio=request.POST.get('bio','').strip()
        profil.sosyal_bildirim='sosyal_bildirim' in request.POST
        profil.etkinlik_bildirim='etkinlik_bildirim' in request.POST
        if 'avatar' in request.FILES: profil.avatar=request.FILES['avatar']
        profil.save()
        messages.success(request,'Profil güncellendi ✅')
        return redirect('profil')
    return render(request,'accounts/profil.html',{
        'profil':profil,'toplam_bagis':toplam_bagis,
        'gonderi_sayisi':gonderi_sayisi,'rozetler':profil.rozet_listesi(),
    })

def hata_404(request, exception):
    return render(request,'errors/404.html',status=404)

def hata_500(request):
    return render(request,'errors/500.html',status=500)
