from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import OnKayit

class DateInput(forms.DateInput):
    input_type = 'date'

class CustomRadioSelect(forms.RadioSelect):
    """Boş seçenek eklemeyen özel RadioSelect widget'ı"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.choices = kwargs.get('choices', [])
    
    def render(self, name, value, attrs=None, renderer=None):
        # Boş seçenek ekleme
        return super().render(name, value, attrs, renderer)
    
    @property
    def input_type(self):
        return 'radio'

class AdminLoginForm(AuthenticationForm):
    """Özel admin login formu"""
    
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Kullanıcı adınızı girin',
            'autocomplete': 'username'
        }),
        label='Kullanıcı Adı'
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Şifrenizi girin',
            'autocomplete': 'current-password'
        }),
        label='Şifre'
    )
    
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        
        if username and password:
            # Kullanıcı var mı kontrol et
            from django.contrib.auth.models import User
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

class OkulKayitFormu(forms.ModelForm):
    class Meta:
        model = OnKayit
        fields = [
            'ogrenci_ad_soyad',
            'ogrenci_tc_kimlik_no',
            'dogum_tarihi',
            'adres',
            'ogrencinin_tuvalet_egitimi',
            'okul_deneyimi_var',
            'okul_devlet_mi',

            'anne_ad_soyad',
            'anne_telefon',
            'anne_ogrenim_durumu',
            'anne_meslek',
            'anne_calisilan_kurum',
            'anne_sag_olu',
            'anne_oz_uvey',
            'anne_aylik_net_gelir',

            'baba_ad_soyad',
            'baba_telefon',
            'baba_ogrenim_durumu',
            'baba_meslek',
            'baba_calisilan_kurum',
            'baba_sag_olu',
            'baba_oz_uvey',
            'baba_aylik_net_gelir',

            'ailedeki_cocuk_sayisi',
            'ikamet_edilen_konut',
            'anne_baba_birliktelik_durumu',
            'velayet_kimde',
            'birinci_kres_tercihi',
            'ikinci_kres_tercihi',
            'ucuncu_kres_tercihi',
            'kvkk_onay',
        ]

        widgets = {
            'birinci_kres_tercihi': forms.Select(choices=[('', 'Seçiniz')] + OnKayit.KRES_CHOICES),
            'ikinci_kres_tercihi': forms.Select(choices=[('', 'Seçiniz')] + OnKayit.KRES_CHOICES),
            'ucuncu_kres_tercihi': forms.Select(choices=[('', 'Seçiniz')] + OnKayit.KRES_CHOICES),
            'dogum_tarihi': DateInput(),
            'ogrencinin_tuvalet_egitimi': forms.RadioSelect(choices=OnKayit.TUVALET_EGITIMI_CHOICES),
            'okul_deneyimi_var': forms.RadioSelect(choices=OnKayit.VAR_YOK_CHOICES),
            'okul_devlet_mi': CustomRadioSelect(choices=OnKayit.DEVLET_OZEL_CHOICES),
            'anne_sag_olu': forms.RadioSelect(choices=OnKayit.SAG_OLU_CHOICES),
            'anne_oz_uvey': forms.RadioSelect(choices=OnKayit.OZ_UVEY_CHOICES),
            'baba_sag_olu': forms.RadioSelect(choices=OnKayit.SAG_OLU_CHOICES),
            'baba_oz_uvey': forms.RadioSelect(choices=OnKayit.OZ_UVEY_CHOICES),
            'ikamet_edilen_konut': forms.RadioSelect(choices=OnKayit.IKAMET_KONUT_CHOICES),
            'anne_baba_birliktelik_durumu': forms.RadioSelect(choices=OnKayit.BIRLIKTELIK_CHOICES),
        }

        labels = {
            'ogrenci_ad_soyad': 'ÖĞRENCİ AD SOYAD',
            'ogrenci_tc_kimlik_no': 'ÖĞRENCİ TC KİMLİK NO',
            'dogum_tarihi': 'DOĞUM TARİHİ',
            'adres': 'ADRES',
            'ogrencinin_tuvalet_egitimi': 'ÖĞRENCİNİN TUVALET EĞİTİMİ (VAR / BEZ KULLANIYOR)',
            'okul_deneyimi_var': 'OKUL DENEYİMİ VAR MI?',
            'okul_devlet_mi': 'VARSA DEVLET YA DA ÖZEL Mİ?',
            'anne_ad_soyad': 'ANNE - ADI SOYADI',
            'anne_telefon': 'ANNE - TELEFON NUMARASI',
            'anne_ogrenim_durumu': 'ANNE - ÖĞRENİM DURUMU',
            'anne_meslek': 'ANNE - MESLEĞİ',
            'anne_calisilan_kurum': 'ANNE - ÇALIŞTIĞI KURUM (AÇIKÇA BELİRTİNİZ)',
            'anne_sag_olu': 'ANNE - SAĞ / ÖLÜ',
            'anne_oz_uvey': 'ANNE - ÖZ / ÜVEY',
            'anne_aylik_net_gelir': 'ANNE - AYLIK NET GELİR',
            'baba_ad_soyad': 'BABA - ADI SOYADI',
            'baba_telefon': 'BABA - TELEFON NUMARASI',
            'baba_ogrenim_durumu': 'BABA - ÖĞRENİM DURUMU',
            'baba_meslek': 'BABA - MESLEĞİ',
            'baba_calisilan_kurum': 'BABA - ÇALIŞTIĞI KURUM (AÇIKÇA BELİRTİNİZ)',
            'baba_sag_olu': 'BABA - SAĞ / ÖLÜ',
            'baba_oz_uvey': 'BABA - ÖZ / ÜVEY',
            'baba_aylik_net_gelir': 'BABA - AYLIK NET GELİR',
            'ailedeki_cocuk_sayisi': 'AİLEDEKİ ÇOCUK SAYISI',
            'ikamet_edilen_konut': 'İKAMET EDİLEN KONUT (KİRACI / EV SAHİBİ)',
            'anne_baba_birliktelik_durumu': 'ANNE BABA BİRLİKTELİK (EVLİ / AYRI)',
            'velayet_kimde': 'VELAYET KİMDE?',
            'birinci_kres_tercihi': 'BİRİNCİ KREŞ TERCİHİ',
            'ikinci_kres_tercihi': 'İKİNCİ KREŞ TERCİHİ',
            'ucuncu_kres_tercihi': 'ÜÇÜNCÜ KREŞ TERCİHİ',
            'kvkk_onay': 'KVKK AYDINLATMA METNİ ONAYI',
        }

        exclude = ['puan', 'kayit_tarihi']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['okul_devlet_mi'].required = False
        # Boş seçenek eklemeyi engelle
        self.fields['okul_devlet_mi'].widget.choices = OnKayit.DEVLET_OZEL_CHOICES
        self.fields['velayet_kimde'].required = False

        # TC Kimlik no 11 hane kontrol için HTML5 pattern
        self.fields['ogrenci_tc_kimlik_no'].widget.attrs.update({
            'placeholder': '11 haneli T.C. Kimlik No',
            'pattern': '^[0-9]{11}$',
            'title': 'Lütfen 11 haneli rakam giriniz.',
            'maxlength': '11',
            'minlength': '11',
            'class': 'form-control',
        })

        # Aylık net gelir alanlarına sadece tam sayı girilsin (virgül istemiyorsun)
        self.fields['anne_aylik_net_gelir'].widget.attrs.update({
            'min': '0',
            'step': '1',
            'oninput': "this.value=this.value.replace(/[^0-9]/g,'')",
            'class': 'form-control',
        })
        self.fields['baba_aylik_net_gelir'].widget.attrs.update({
            'min': '0',
            'step': '1',
            'oninput': "this.value=this.value.replace(/[^0-9]/g,'')",
            'class': 'form-control',
        })

        # Öğrenim durumu seçimleri (dropdown/select) - sadece class ekle
        self.fields['anne_ogrenim_durumu'].widget.attrs.update({'class': 'form-select'})
        self.fields['baba_ogrenim_durumu'].widget.attrs.update({'class': 'form-select'})

        # Place holderlar
        self.fields['ogrenci_ad_soyad'].widget.attrs.update({'placeholder': 'Ad Soyad', 'class': 'form-control'})
        self.fields['adres'].widget.attrs.update({'placeholder': 'Mahalle, cadde, sokak, no, il/ilçe', 'class': 'form-control'})

        # Diğer tüm input, textarea ve select alanlarına class ekle (varsa üzerine yazmaz)
        for name, field in self.fields.items():
            if field.widget.__class__.__name__ in ['TextInput', 'NumberInput', 'EmailInput', 'DateInput', 'Textarea']:
                field.widget.attrs.setdefault('class', 'form-control')
            elif field.widget.__class__.__name__ in ['Select']:
                field.widget.attrs.setdefault('class', 'form-select')
            elif field.widget.__class__.__name__ in ['RadioSelect']:
                field.widget.attrs.setdefault('class', 'form-check-input')
            elif field.widget.__class__.__name__ in ['CheckboxInput']:
                field.widget.attrs.setdefault('class', 'form-check-input')
