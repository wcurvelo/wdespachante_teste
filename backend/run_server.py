#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

if __name__ == '__main__':
    try:
        print("Carregando aplicativo Flask...")
        from app import app
        
        print("Configurações atuais:")
        print(f"- Limite de vídeo: {app.config.get('MAX_VIDEO_SIZE', 0) / (1024*1024):.0f}MB")
        print(f"- Limite geral: {app.config.get('MAX_CONTENT_LENGTH', 0) / (1024*1024):.0f}MB")
        print(f"- Formatos de vídeo: {app.config.get('ALLOWED_VIDEO_EXTENSIONS', 'N/A')}")
        
        print("\nIniciando servidor...")
        print("Acesse: http://localhost:5000")
        print("Admin: http://localhost:5000/admin")
        print("Login: admin / admin")
        print("Pressione Ctrl+C para parar")
        
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
        
    except Exception as e:
        print(f"Erro ao iniciar o servidor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)