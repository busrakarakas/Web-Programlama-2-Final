from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Veteriner,Randevu

def liste(request):
    vets=Veteriner.objects.filter(aktif=True)
    return render(request,'veteriner/liste.html',{'vets':vets})

@login_required
def randevu(request,pk):
    vet=get_object_or_404(Veteriner,pk=pk,aktif=True)
    if request.method=='POST':
        Randevu.objects.create(veteriner=vet,kullanici=request.user,hayvan_adi=request.POST.get('hayvan_adi','').strip(),sahip_adi=request.POST.get('sahip_adi','').strip(),telefon=request.POST.get('telefon','').strip(),tarih=request.POST.get('tarih'),neden=request.POST.get('neden','').strip())
        messages.success(request,f'"{vet.isim}" kliniğine randevu talebiniz iletildi! ✅')
        return redirect('veteriner')
    return render(request,'veteriner/randevu.html',{'vet':vet})

@login_required
def randevularim(request):
    randevular=Randevu.objects.filter(kullanici=request.user).select_related('veteriner')
    return render(request,'veteriner/randevularim.html',{'randevular':randevular})
