# kayit_formu/urls.py

from django.urls import path # <-- SADECE path OLMALI, include'a gerek yok
from . import views # Uygulamanın views.py dosyasını import ediyoruz

app_name = 'kayit_formu' # Bu uygulamanın URL'leri için bir namespace (isim alanı) belirleriz

urlpatterns = [
    path('', views.on_kayit_formu, name='on_kayit_formu_ana'), # Ana sayfa doğrudan ön kayıt formuna gider
    path('on-kayit/', views.on_kayit_formu, name='on_kayit_formu'), # Ön kayıt formu sayfası
    path('kayit-basarili/', views.kayit_basarili, name='kayit_basarili'), # Kayıt başarılı sayfası
    path('kayitlar/', views.admin_kayit_listesi, name='admin_kayit_listesi'), # Kayıt listesi (giriş gerektirir)
    path('kayitlar/<int:pk>/', views.kayit_detay, name='kayit_detay'), # Başvuru detay sayfası
    path('admin-login/', views.admin_login_view, name='admin_login'), # Özel admin login
]