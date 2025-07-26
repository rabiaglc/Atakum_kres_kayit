# kayit_formu/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import OkulKayitFormu
from .models import OnKayit
from django.contrib.auth.decorators import login_required


def on_kayit_formu(request):
    if request.method == 'POST':
        form = OkulKayitFormu(request.POST)
        if form.is_valid():
            on_kayit = form.save(commit=False)
            on_kayit.save()
            on_kayit.calculate_score()
            # Başarılı sayfasına yönlendiriyoruz, URL namespace varsa onunla kullan
            return redirect(reverse('kayit_formu:kayit_basarili'))
    else:
        form = OkulKayitFormu()

    return render(request, 'kayit_formu/on_kayit_formu.html', {'form': form})


def kayit_basarili(request):
    # Kayıt başarılı olduktan sonra gösterilen basit onay sayfası
    return render(request, 'kayit_formu/kayit_basarili.html')


@login_required
def admin_kayit_listesi(request):
    # Tüm kayıtları listeleyen sayfa (istersen admin panel yerine bunu kullanabilirsin)
    kayitlar = OnKayit.objects.all().order_by('-kayit_tarihi')
    return render(request, 'kayit_formu/admin_kayit_listesi.html', {'kayitlar': kayitlar})


@login_required
def kayit_detay(request, pk):
    kayit = get_object_or_404(OnKayit, pk=pk)
    return render(request, 'kayit_formu/kayit_detay.html', {'kayit': kayit})
