from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import getpass
import re

class Command(BaseCommand):
    help = 'Güvenli admin kullanıcısı oluşturur'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, help='Kullanıcı adı')
        parser.add_argument('--email', type=str, help='E-posta adresi')

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Güvenli Admin Kullanıcısı Oluşturma ==='))
        
        # Kullanıcı adı al
        username = options['username']
        if not username:
            username = input('Kullanıcı adı: ').strip()
        
        if not username:
            self.stdout.write(self.style.ERROR('Kullanıcı adı boş olamaz!'))
            return
        
        # Kullanıcı zaten var mı kontrol et
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.ERROR(f'"{username}" kullanıcı adı zaten kullanılıyor!'))
            return
        
        # E-posta al
        email = options['email']
        if not email:
            email = input('E-posta adresi: ').strip()
        
        # Şifre al
        while True:
            password = getpass.getpass('Şifre: ')
            password_confirm = getpass.getpass('Şifre (tekrar): ')
            
            if password != password_confirm:
                self.stdout.write(self.style.ERROR('Şifreler eşleşmiyor!'))
                continue
            
            # Şifre güvenliği kontrolü
            try:
                validate_password(password)
            except ValidationError as e:
                self.stdout.write(self.style.ERROR(f'Şifre güvenliği: {e.messages[0]}'))
                continue
            
            # Ek güvenlik kontrolleri
            if len(password) < 12:
                self.stdout.write(self.style.ERROR('Şifre en az 12 karakter olmalıdır!'))
                continue
            
            if not re.search(r'[A-Z]', password):
                self.stdout.write(self.style.ERROR('Şifre en az bir büyük harf içermelidir!'))
                continue
            
            if not re.search(r'[a-z]', password):
                self.stdout.write(self.style.ERROR('Şifre en az bir küçük harf içermelidir!'))
                continue
            
            if not re.search(r'\d', password):
                self.stdout.write(self.style.ERROR('Şifre en az bir rakam içermelidir!'))
                continue
            
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
                self.stdout.write(self.style.ERROR('Şifre en az bir özel karakter içermelidir!'))
                continue
            
            break
        
        # Kullanıcıyı oluştur
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=True,
                is_superuser=True
            )
            
            self.stdout.write(self.style.SUCCESS(f'✅ Güvenli admin kullanıcısı oluşturuldu!'))
            self.stdout.write(f'   Kullanıcı adı: {username}')
            self.stdout.write(f'   E-posta: {email}')
            self.stdout.write(f'   Şifre güvenlik seviyesi: Yüksek')
            self.stdout.write('')
            self.stdout.write('🔐 Güvenlik Önerileri:')
            self.stdout.write('   - Şifrenizi güvenli bir yerde saklayın')
            self.stdout.write('   - İki faktörlü doğrulama kullanın')
            self.stdout.write('   - Düzenli olarak şifrenizi değiştirin')
            self.stdout.write('   - Admin paneline sadece güvenli ağlardan erişin')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Kullanıcı oluşturulurken hata: {e}')) 