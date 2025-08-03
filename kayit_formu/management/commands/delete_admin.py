from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Admin kullanıcısını siler'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='admin', help='Silinecek kullanıcı adı')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            user = User.objects.get(username=username)
            
            # Kullanıcı bilgilerini göster
            self.stdout.write(f"Kullanıcı bulundu:")
            self.stdout.write(f"  Kullanıcı adı: {user.username}")
            self.stdout.write(f"  E-posta: {user.email}")
            self.stdout.write(f"  Superuser: {user.is_superuser}")
            self.stdout.write(f"  Staff: {user.is_staff}")
            
            # Onay al
            confirm = input(f"\n'{username}' kullanıcısını silmek istediğinizden emin misiniz? (evet/hayır): ")
            
            if confirm.lower() in ['evet', 'yes', 'y', 'e']:
                user.delete()
                self.stdout.write(self.style.SUCCESS(f"✅ '{username}' kullanıcısı başarıyla silindi!"))
            else:
                self.stdout.write(self.style.WARNING("❌ İşlem iptal edildi."))
                
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"❌ '{username}' kullanıcısı bulunamadı!"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Hata: {e}")) 