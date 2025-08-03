from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from .models import OnKayit

# Register your models here.

class CustomAdminLoginForm(AuthenticationForm):
    """Özel admin login formu"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Kullanıcı adınızı girin',
            'autocomplete': 'username',
            'id': 'id_username'
        }),
        label='Kullanıcı Adı'
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Şifrenizi girin',
            'autocomplete': 'current-password',
            'id': 'id_password'
        }),
        label='Şifre'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            # Kullanıcı var mı kontrol et
            try:
                user = User.objects.get(username=username)
                if not user.is_active:
                    raise forms.ValidationError(
                        "Bu kullanıcı hesabı devre dışı bırakılmış. Lütfen sistem yöneticisi ile iletişime geçin."
                    )
                if not user.is_staff:
                    raise forms.ValidationError(
                        "Bu kullanıcı adı ile yönetici paneline erişim yetkiniz bulunmamaktadır."
                    )
            except User.DoesNotExist:
                raise forms.ValidationError(
                    "Kullanıcı adı bulunamadı. Lütfen kullanıcı adınızı kontrol edin."
                )
        
        return cleaned_data

@admin.register(OnKayit)
class OnKayitAdmin(admin.ModelAdmin):
    list_display = ['ogrenci_ad_soyad', 'ogrenci_tc_kimlik_no', 'kres_tercihleri', 'kayit_tarihi', 'puan']
    list_filter = ['kayit_tarihi', 'birinci_kres_tercihi', 'ikinci_kres_tercihi', 'ucuncu_kres_tercihi']
    search_fields = ['ogrenci_ad_soyad', 'ogrenci_tc_kimlik_no', 'anne_ad_soyad', 'baba_ad_soyad']
    readonly_fields = ['kayit_tarihi', 'puan']
    ordering = ['-kayit_tarihi']
    
    fieldsets = (
        ('Kreş Tercihleri', {
            'fields': ('birinci_kres_tercihi', 'ikinci_kres_tercihi', 'ucuncu_kres_tercihi')
        }),
        ('Öğrenci Bilgileri', {
            'fields': ('ogrenci_ad_soyad', 'ogrenci_tc_kimlik_no', 'dogum_tarihi', 'adres', 
                      'ogrencinin_tuvalet_egitimi', 'okul_deneyimi_var', 'okul_devlet_mi')
        }),
        ('Anne Bilgileri', {
            'fields': ('anne_ad_soyad', 'anne_telefon', 'anne_ogrenim_durumu', 'anne_meslek', 
                      'anne_calisilan_kurum', 'anne_sag_olu', 'anne_oz_uvey', 'anne_aylik_net_gelir')
        }),
        ('Baba Bilgileri', {
            'fields': ('baba_ad_soyad', 'baba_telefon', 'baba_ogrenim_durumu', 'baba_meslek', 
                      'baba_calisilan_kurum', 'baba_sag_olu', 'baba_oz_uvey', 'baba_aylik_net_gelir')
        }),
        ('Aile Bilgileri', {
            'fields': ('ailedeki_cocuk_sayisi', 'ikamet_edilen_konut', 'anne_baba_birliktelik_durumu', 'velayet_kimde')
        }),
        ('Sistem Bilgileri', {
            'fields': ('kayit_tarihi', 'puan'),
            'classes': ('collapse',)
        }),
    )
    
    def kres_tercihleri(self, obj):
        return f"1.{obj.get_birinci_kres_tercihi_display()} | 2.{obj.get_ikinci_kres_tercihi_display()} | 3.{obj.get_ucuncu_kres_tercihi_display()}"
    kres_tercihleri.short_description = 'Kreş Tercihleri'
    
    def has_add_permission(self, request):
        # Sadece superuser yeni kayıt ekleyebilir
        return request.user.is_superuser
    
    def has_delete_permission(self, request, obj=None):
        # Sadece superuser kayıt silebilir
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj=None):
        # Sadece staff kullanıcılar düzenleyebilir
        return request.user.is_staff

# Admin site başlıklarını özelleştir
admin.site.site_header = "Atakum Kreş Yönetim Paneli"
admin.site.site_title = "Atakum Kreş Admin"
admin.site.index_title = "Kreş Kayıt Yönetimi"

# Admin login formunu özelleştir
admin.site.login_form = CustomAdminLoginForm
