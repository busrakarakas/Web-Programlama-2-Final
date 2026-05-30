from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import Gonderi,GonderiBegeni,Yorum,Anket,AnketSecenek,AnketOy,Sohbet,Mesaj

TREND=['#sokakcanları','#cumartesikeyfi','#mamadesteği','#mutlupatiler','#köpekseverleri','#kediseverleri','#sahiplendirme','#barınak']

def akis(request):
    gonderiler=Gonderi.objects.select_related('yazar__profil').prefetch_related('begeniler','yorumlar__yazar','anket__secenekler').order_by('-olusturuldu')
    data=[]
    for g in gonderiler:
        oyu=None
        if hasattr(g,'anket'): oyu=g.anket.kullanici_oyu(request.user)
        data.append({'g':g,'begendi':g.kullanici_begendi_mi(request.user),'kullanici_oyu':oyu})
    return render(request,'sosyal/akis.html',{'data':data,'trend':TREND})

@login_required
@require_POST
def gonderi_olustur(request):
    icerik=request.POST.get('icerik','').strip()
    resim=request.FILES.get('resim')
    if not icerik and not resim:
        messages.error(request,'Gönderi boş olamaz.')
        return redirect('akis')
    Gonderi.objects.create(yazar=request.user,icerik=icerik,resim=resim)
    messages.success(request,'Gönderi paylaşıldı! 🐾')
    return redirect('akis')

@login_required
@require_POST
def anket_olustur(request):
    soru=request.POST.get('soru','').strip()
    opts=[request.POST.get(f's{i}','').strip() for i in range(1,6)]
    opts=[o for o in opts if o]
    if not soru or len(opts)<2:
        messages.error(request,'Soru ve en az 2 seçenek gerekli.')
        return redirect('akis')
    with transaction.atomic():
        g=Gonderi.objects.create(yazar=request.user,icerik='')
        a=Anket.objects.create(gonderi=g,yazar=request.user,soru=soru)
        for i,m in enumerate(opts): AnketSecenek.objects.create(anket=a,metin=m,sira=i)
    messages.success(request,'Anket oluşturuldu! 🗳️')
    return redirect('akis')

@login_required
@require_POST
def oy_ver(request,pk):
    anket=get_object_or_404(Anket,pk=pk)
    if anket.kullanici_oyu(request.user): return JsonResponse({'hata':'Zaten oy kullandınız.'},status=400)
    sid=request.POST.get('sid')
    secenek=get_object_or_404(AnketSecenek,pk=sid,anket=anket)
    with transaction.atomic():
        AnketOy.objects.create(anket=anket,secenek=secenek,kullanici=request.user)
        AnketSecenek.objects.filter(pk=sid).update(oy_sayisi=secenek.oy_sayisi+1)
    anket.refresh_from_db()
    sonuc=[]
    for s in anket.secenekler.all():
        s.refresh_from_db()
        sonuc.append({'id':s.pk,'metin':s.metin,'oy':s.oy_sayisi,'pct':s.yuzde(),'secildi':s.pk==secenek.pk})
    return JsonResponse({'toplam':anket.toplam_oy(),'sonuc':sonuc})

@login_required
@require_POST
def begen(request,pk):
    g=get_object_or_404(Gonderi,pk=pk)
    obj,created=GonderiBegeni.objects.get_or_create(gonderi=g,kullanici=request.user)
    if not created: obj.delete()
    return JsonResponse({'begendi':created,'sayi':g.begeni_sayisi()})

@login_required
@require_POST
def yorum_ekle(request,pk):
    g=get_object_or_404(Gonderi,pk=pk)
    metin=request.POST.get('metin','').strip()
    if not metin: return JsonResponse({'hata':'Boş yorum.'},status=400)
    y=Yorum.objects.create(gonderi=g,yazar=request.user,metin=metin)
    ad=request.user.get_full_name() or request.user.username
    return JsonResponse({'yazar':ad,'harf':ad[0].upper(),'metin':y.metin,'sayi':g.yorum_sayisi()})

def sohbet(request):
    kanallar=Sohbet.objects.filter(kanal=True).prefetch_related('mesajlar')
    dmler=request.user.sohbetler.filter(kanal=False) if request.user.is_authenticated else []
    sid=request.GET.get('s')
    aktif=None; mesajlar=[]
    if sid: aktif=get_object_or_404(Sohbet,pk=sid)
    elif kanallar.exists(): aktif=kanallar.first()
    if aktif: mesajlar=aktif.mesajlar.select_related('gonderen').all()
    return render(request,'sosyal/sohbet.html',{'kanallar':kanallar,'dmler':dmler,'aktif':aktif,'mesajlar':mesajlar})

@login_required
@require_POST
def mesaj_gonder(request,pk):
    s=get_object_or_404(Sohbet,pk=pk)
    metin=request.POST.get('metin','').strip()
    if not metin: return JsonResponse({'hata':'Boş mesaj.'},status=400)
    m=Mesaj.objects.create(sohbet=s,gonderen=request.user,metin=metin)
    ad=request.user.get_full_name() or request.user.username
    return JsonResponse({'metin':m.metin,'gonderen':ad,'harf':ad[0].upper(),'saat':m.gonderildi.strftime('%H:%M')})
