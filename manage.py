#!/usr/bin/env python
"""
🐾 Evcil Hayvan Platformu - Django Management Utility
==============================================================================
Bu dosya, Django projesinin yönetim komutlarını çalıştırır.
Environment detection ve error handling ile zenginleştirilmiştir.
==============================================================================
"""

import os
import sys
from pathlib import Path

def main():
    """Django management komutlarını çalıştır"""
    
    # Environment detection
    environment = os.getenv('DJANGO_ENVIRONMENT', 'development').lower()
    
    # Settings modülünü belirle
    settings_modules = {
        'development': 'config.settings.development',
        'testing': 'config.settings.testing', 
        'production': 'config.settings.production',
    }
    
    settings_module = settings_modules.get(environment, 'config.settings')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
    
    # Project structure validation
    base_dir = Path(__file__).resolve().parent
    required_dirs = [
        base_dir / 'apps',
        base_dir / 'logs',
        base_dir / 'media',
        base_dir / 'static',
        base_dir / 'templates',
    ]
    
    for directory in required_dirs:
        if not directory.exists():
            directory.mkdir(parents=True, exist_ok=True)
    
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django import edilemedi! Django yüklü olduğundan ve "
            "virtual environment'ın aktif olduğundan emin olun."
        ) from exc
    
    # Development helpers
    if environment == 'development' and len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'runserver':
            print(f"""
🐾 ===============================================
   Evcil Hayvan Platformu Development Server
===============================================

🌍 Environment: {environment.upper()}
⚙️  Settings: {settings_module}

💝 Sevgi dolu geliştirme başlıyor!
===============================================
            """)
    
    try:
        execute_from_command_line(sys.argv)
    except KeyboardInterrupt:
        print("\n🐾 Platform yönetimi durduruldu. Güle güle! 💝")
        sys.exit(0)
    except Exception as e:
        print(f"""
        🚨 ===============================================
           KOMUT ÇALIŞTIRMA HATASI!
        ===============================================
        
        Hata: {str(e)}
        Environment: {environment}
        Settings: {settings_module}
        
        Destek için: destek@evcilhayvanplatformu.com
        ===============================================
        """)
        
        # Development'ta detaylı hata, production'da minimal
        if environment == 'development':
            raise
        else:
            sys.exit(1)

# ==============================================================================
# 🎯 CUSTOM MANAGEMENT COMMANDS - Özel yönetim komutları
# ==============================================================================

def setup_custom_commands():
    """
    Platform özel management komutları için hazırlık
    """
    # Custom commands directory
    commands_dir = Path(__file__).resolve().parent / 'apps' / 'ortak' / 'management' / 'commands'
    commands_dir.mkdir(parents=True, exist_ok=True)
    
    # __init__.py dosyalarını oluştur
    for path in [
        commands_dir.parent.parent / '__init__.py',
        commands_dir.parent / '__init__.py',
        commands_dir / '__init__.py'
    ]:
        if not path.exists():
            path.touch()

if __name__ == '__main__':
    # Custom commands setup
    setup_custom_commands()
    
    # Ana management fonksiyonunu çalıştır
    main()
