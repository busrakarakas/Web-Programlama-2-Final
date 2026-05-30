from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.db.models import Sum
from decimal import Decimal,InvalidOperation
from .models import Kampanya,Bagis

def bagis_view(request):
    kampanyalar=Kampanya.objects.filter(aktif=True)
    son_bagislar=Bagis.objects.select_related('kullanici','kampanya').order_by('-tarih')[:10]
    aylik_hedef=Decimal('10000')
    aylik_toplanan=Bagis.objects.aggregate(t=Sum('miktar'))['t'] or Decimal('0')
    aylik_yuzde=min(100,round(float(aylik_toplanan)/float(aylik_hedef)*100))
    if request.method=='POST':
        try:
            miktar=Decimal(request.POST.get('miktar','0'))
            if miktar<=0: raise ValueError
        except (InvalidOperation,ValueError):
            messages.error(request,'Lütfen geçerli bir miktar girin.')
            return redirect('bagis')
        kid=request.POST.get('kampanya_id') or None
        kampanya=get_object_or_404(Kampanya,pk=kid) if kid else None
        ad=request.user.get_full_name() or request.user.username if request.user.is_authenticated else request.POST.get('ad_soyad','').strip() or 'Anonim'
        Bagis.objects.create(kullanici=request.user if request.user.is_authenticated else None,kampanya=kampanya,miktar=miktar,ad_soyad=ad)
        if kampanya:
            kampanya.toplanan+=miktar; kampanya.save()
        if request.user.is_authenticated:
            from accounts.models import Rozet
            Rozet.objects.get_or_create(kullanici=request.user,tur='comert_pati')
        hedef=f'"{kampanya.baslik}" kampanyasına' if kampanya else 'Genel fona'
        messages.success(request,f'{hedef} {miktar}₺ bağışınız alındı! Teşekkürler 💜')
        return redirect('bagis')
    return render(request,'bagis/bagis.html',{'kampanyalar':kampanyalar,'son_bagislar':son_bagislar,'aylik_hedef':aylik_hedef,'aylik_toplanan':aylik_toplanan,'aylik_yuzde':aylik_yuzde})
