from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import re

class AdminSecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Admin URL'lerini kontrol et
        if self.is_admin_url(request.path):
            # Login sayfasına erişime izin ver
            if request.path.endswith('/login/'):
                response = self.get_response(request)
                return response
            
            # Kullanıcı giriş yapmamışsa login sayfasına yönlendir
            if not request.user.is_authenticated:
                return redirect('admin:login')
            
            # Kullanıcı staff değilse erişimi engelle
            if not request.user.is_staff:
                messages.error(request, 'Bu sayfaya erişim yetkiniz bulunmamaktadır.')
                return redirect('/')
            
            # Brute force saldırılarına karşı koruma
            if self.is_brute_force_attempt(request):
                messages.error(request, 'Çok fazla başarısız giriş denemesi. Lütfen daha sonra tekrar deneyin.')
                return redirect('/')
        
        response = self.get_response(request)
        return response

    def is_admin_url(self, path):
        """Admin URL'lerini kontrol et"""
        admin_patterns = [
            r'^/yonetim-paneli/',
            r'^/admin/',
        ]
        # Login sayfasına her zaman izin ver
        if path.endswith('/login/') or 'login' in path:
            return False
        return any(re.match(pattern, path) for pattern in admin_patterns)

    def is_brute_force_attempt(self, request):
        """Brute force saldırısı kontrolü"""
        # Session'da başarısız giriş sayısını kontrol et
        failed_attempts = request.session.get('failed_login_attempts', 0)
        last_attempt_str = request.session.get('last_failed_attempt')
        
        # 5 dakika içinde 5'ten fazla başarısız giriş varsa engelle
        if last_attempt_str and failed_attempts >= 5:
            try:
                from datetime import datetime
                last_attempt = datetime.fromisoformat(last_attempt_str.replace('Z', '+00:00'))
                time_diff = timezone.now() - last_attempt
                if time_diff < timedelta(minutes=5):
                    return True
            except (ValueError, TypeError):
                pass
        
        return False

class LoginAttemptMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Login sayfasında başarısız giriş varsa sayacı artır
        if request.path.endswith('/login/') and request.method == 'POST':
            # Form hatalarını güvenli şekilde kontrol et
            try:
                if hasattr(response, 'context_data') and response.context_data:
                    form = response.context_data.get('form')
                    if form and hasattr(form, 'errors') and form.errors:
                        self.record_failed_attempt(request)
            except Exception:
                pass  # Hata durumunda sessizce geç
        
        return response

    def record_failed_attempt(self, request):
        """Başarısız giriş denemesini kaydet"""
        failed_attempts = request.session.get('failed_login_attempts', 0)
        request.session['failed_login_attempts'] = failed_attempts + 1
        request.session['last_failed_attempt'] = timezone.now().isoformat()
        request.session.modified = True

class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Güvenlik başlıkları ekle
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response 