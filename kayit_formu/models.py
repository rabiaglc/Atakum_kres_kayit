from django.db import models


class OnKayit(models.Model):
    # === Kreş Tercihleri ===
    KRES_CHOICES = [
        ('secenek_1', 'Seçenek 1'),
        ('secenek_2', 'Seçenek 2'),
        ('secenek_3', 'Seçenek 3'),
        ('secenek_4', 'Seçenek 4'),
    ]
    birinci_kres_tercihi = models.CharField(
        max_length=20,
        choices=KRES_CHOICES,
        blank=True,
        null=True,
        verbose_name="Birinci Kreş Tercihi"
    )
    ikinci_kres_tercihi = models.CharField(
        max_length=20,
        choices=KRES_CHOICES,
        blank=True,
        null=True,
        verbose_name="İkinci Kreş Tercihi"
    )
    ucuncu_kres_tercihi = models.CharField(
        max_length=20,
        choices=KRES_CHOICES,
        blank=True,
        null=True,
        verbose_name="Üçüncü Kreş Tercihi"
    )
    
    # KVKK Aydınlatma Metni Onayı
    kvkk_onay = models.BooleanField(
        default=False,
        verbose_name="KVKK Aydınlatma Metni Onayı",
        help_text="Kişisel Verilerin Korunması Kanunu kapsamında aydınlatma metnini okudum ve onaylıyorum."
    )

    # === Öğrenci Bilgileri ===
    ogrenci_ad_soyad = models.CharField(max_length=200, verbose_name="Öğrenci Ad Soyad")
    ogrenci_tc_kimlik_no = models.CharField(
        max_length=11,
        unique=True,
        verbose_name="Öğrenci T.C. Kimlik No",
        blank=False,
        null=False,
    )
    dogum_tarihi = models.DateField(verbose_name="Doğum Tarihi")
    adres = models.TextField(verbose_name="Adres")

    TUVALET_EGITIMI_CHOICES = [
        (True, 'VAR'),
        (False, 'BEZ KULLANIYOR'),
    ]
    ogrencinin_tuvalet_egitimi = models.BooleanField(
        choices=TUVALET_EGITIMI_CHOICES,
        default=False,
        verbose_name="Öğrencinin Tuvalet Eğitimi"
    )

    VAR_YOK_CHOICES = [
        (True, 'VAR'),
        (False, 'YOK'),
    ]
    okul_deneyimi_var = models.BooleanField(
        choices=VAR_YOK_CHOICES,
        default=False,
        verbose_name="Okul Deneyimi Var Mı?"
    )

    DEVLET_OZEL_CHOICES = [
        ('devlet', 'DEVLET'),
        ('ozel', 'ÖZEL'),
    ]
    okul_devlet_mi = models.CharField(
        max_length=10,
        choices=DEVLET_OZEL_CHOICES,
        blank=True,
        null=True,
        verbose_name="Varsa Devlet Ya Da Özel Mi?"
    )

    # === Aile Bilgileri: Anne ===
    SAG_OLU_CHOICES = [
        ('sag', 'SAĞ'),
        ('olu', 'ÖLÜ'),
    ]
    OZ_UVEY_CHOICES = [
        ('oz', 'ÖZ'),
        ('uvey', 'ÜVEY'),
    ]
    OGRENIM_DURUMU_CHOICES = [
        ('ilkogretim', 'İlköğretim'),
        ('ortaokul', 'Ortaokul'),
        ('lise', 'Lise'),
        ('universite', 'Üniversite'),
        ('yukseklisans', 'Yüksek Lisans'),
        ('doktora', 'Doktora'),
    ]

    anne_ad_soyad = models.CharField(max_length=200, verbose_name="Anne - Adı Soyadı")
    anne_telefon = models.CharField(max_length=15, verbose_name="Anne - Telefon Numarası")
    anne_ogrenim_durumu = models.CharField(
        max_length=20,
        choices=OGRENIM_DURUMU_CHOICES,
        verbose_name="Anne - Öğrenim Durumu"
    )
    anne_meslek = models.CharField(max_length=100, verbose_name="Anne - Mesleği")
    anne_calisilan_kurum = models.CharField(max_length=200, blank=True, null=True, verbose_name="Anne - Çalıştığı Kurum")
    anne_sag_olu = models.CharField(
        max_length=3,
        choices=SAG_OLU_CHOICES,
        default='sag',
        verbose_name="Anne - Sağ / Ölü"
    )
    anne_oz_uvey = models.CharField(
        max_length=4,
        choices=OZ_UVEY_CHOICES,
        default='oz',
        verbose_name="Anne - Öz / Üvey"
    )
    anne_aylik_net_gelir = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name="Anne - Aylık Net Gelir",
        default=0
    )

    # === Aile Bilgileri: Baba ===
    baba_ad_soyad = models.CharField(max_length=200, verbose_name="Baba - Adı Soyadı")
    baba_telefon = models.CharField(max_length=15, verbose_name="Baba - Telefon Numarası")
    baba_ogrenim_durumu = models.CharField(
        max_length=20,
        choices=OGRENIM_DURUMU_CHOICES,
        verbose_name="Baba - Öğrenim Durumu"
    )
    baba_meslek = models.CharField(max_length=100, verbose_name="Baba - Mesleği")
    baba_calisilan_kurum = models.CharField(max_length=200, blank=True, null=True, verbose_name="Baba - Çalıştığı Kurum")
    baba_sag_olu = models.CharField(
        max_length=3,
        choices=SAG_OLU_CHOICES,
        default='sag',
        verbose_name="Baba - Sağ / Ölü"
    )
    baba_oz_uvey = models.CharField(
        max_length=4,
        choices=OZ_UVEY_CHOICES,
        default='oz',
        verbose_name="Baba - Öz / Üvey"
    )
    baba_aylik_net_gelir = models.DecimalField(
        max_digits=10,
        decimal_places=0,
        verbose_name="Baba - Aylık Net Gelir",
        default=0
    )

    # === Genel Aile Bilgileri ===
    ailedeki_cocuk_sayisi = models.IntegerField(verbose_name="Ailedeki Çocuk Sayısı", default=1)

    IKAMET_KONUT_CHOICES = [
        ('kiraci', 'KİRACI'),
        ('ev_sahibi', 'EV SAHİBİ'),
    ]
    ikamet_edilen_konut = models.CharField(
        max_length=15,
        choices=IKAMET_KONUT_CHOICES,
        default='kiraci',
        verbose_name="İkamet Edilen Konut"
    )

    BIRLIKTELIK_CHOICES = [
        ('evli', 'EVLİ'),
        ('ayri', 'AYRI'),
    ]
    anne_baba_birliktelik_durumu = models.CharField(
        max_length=10,
        choices=BIRLIKTELIK_CHOICES,
        default='evli',
        verbose_name="Anne Baba Birliktelik Durumu"
    )
    velayet_kimde = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        default='',
        verbose_name="Velayet Kimde?"
    )

    # === Sistem Bilgileri ===
    kayit_tarihi = models.DateTimeField(auto_now_add=True)
    puan = models.IntegerField(default=0)

    def calculate_score(self):
        score = 0
        if self.anne_ogrenim_durumu in ['universite', 'yukseklisans', 'doktora']:
            score += 10
        if self.baba_ogrenim_durumu in ['universite', 'yukseklisans', 'doktora']:
            score += 5
        if self.anne_calisilan_kurum and self.anne_calisilan_kurum.strip():
            score += 15
        if self.baba_calisilan_kurum and self.baba_calisilan_kurum.strip():
            score += 10
        if self.anne_aylik_net_gelir < 15000:
            score += 3
        if self.baba_aylik_net_gelir < 15000:
            score += 2
        if self.ailedeki_cocuk_sayisi >= 3:
            score += 3
        elif self.ailedeki_cocuk_sayisi == 2:
            score += 1
        if self.ikamet_edilen_konut == 'kiraci':
            score += 2
        if self.anne_baba_birliktelik_durumu == 'ayri':
            score += 5

        self.puan = score
        self.save()

    def __str__(self):
        return f"{self.ogrenci_ad_soyad} - {self.kayit_tarihi.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name = "Ön Kayıt"
        verbose_name_plural = "Ön Kayıtlar"
