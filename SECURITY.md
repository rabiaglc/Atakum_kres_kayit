# 🔐 Atakum Kreş Admin Güvenlik Kılavuzu

## Güvenlik Önlemleri

### 1. Admin URL Gizleme
- Admin paneli URL'i `/admin/` yerine `/yonetim-paneli/` olarak değiştirildi
- Bu sayede otomatik bot saldırılarına karşı koruma sağlanır

### 2. Güçlü Şifre Politikası
- Minimum 12 karakter
- En az 1 büyük harf
- En az 1 küçük harf  
- En az 1 rakam
- En az 1 özel karakter

### 3. Brute Force Koruması
- 5 dakika içinde 5 başarısız giriş denemesi sonrası geçici engelleme
- Session tabanlı giriş denemesi takibi

### 4. Güvenlik Başlıkları
- X-Content-Type-Options: nosniff
- X-Frame-Options: DENY
- X-XSS-Protection: 1; mode=block
- Referrer-Policy: strict-origin-when-cross-origin

### 5. Yetki Kontrolü
- Sadece staff kullanıcılar admin paneline erişebilir
- Sadece superuser yeni kayıt ekleyebilir/silebilir
- Normal staff kullanıcılar sadece görüntüleyebilir/düzenleyebilir

## Kullanım

### Güvenli Admin Kullanıcısı Oluşturma
```bash
python manage.py secure_admin
```

### Admin Paneline Erişim
- URL: `http://yourdomain.com/yonetim-paneli/`
- Kullanıcı adı ve güçlü şifre ile giriş yapın

### Güvenlik Önerileri

1. **Şifre Yönetimi**
   - Güçlü şifreler kullanın
   - Şifreleri düzenli olarak değiştirin
   - Şifreleri güvenli bir yerde saklayın

2. **Erişim Kontrolü**
   - Admin paneline sadece güvenli ağlardan erişin
   - Ortak bilgisayarlarda "Beni Hatırla" seçeneğini kullanmayın
   - İşlem sonrası mutlaka çıkış yapın

3. **Sistem Güvenliği**
   - Sunucunuzu güncel tutun
   - Güvenlik duvarı kullanın
   - SSL sertifikası kullanın (HTTPS)

4. **Yedekleme**
   - Veritabanını düzenli olarak yedekleyin
   - Yedekleri güvenli bir yerde saklayın

## Acil Durumlar

### Şifre Unutuldu
```bash
python manage.py changepassword <username>
```

### Kullanıcı Kilitleme
```bash
python manage.py shell
>>> from django.contrib.auth.models import User
>>> user = User.objects.get(username='<username>')
>>> user.is_active = False
>>> user.save()
```

### Güvenlik İhlali Durumunda
1. Tüm admin kullanıcılarının şifrelerini değiştirin
2. Sunucu loglarını kontrol edin
3. Şüpheli aktiviteleri raporlayın
4. Gerekirse sistem yöneticisi ile iletişime geçin

## Log Takibi

Admin paneline yapılan tüm girişler ve işlemler otomatik olarak loglanır:
- Başarısız giriş denemeleri
- Başarılı girişler
- Veri değişiklikleri
- Silme işlemleri

## İletişim

Güvenlik sorunları için:
- E-posta: security@atakumkres.com
- Telefon: +90 XXX XXX XX XX
- Acil durum: 7/24 destek hattı 