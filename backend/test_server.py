#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask

# Criar uma aplicação Flask simples para teste
test_app = Flask(__name__)

@test_app.route('/')
def hello():
    return '''
    <h1>Servidor Flask Funcionando!</h1>
    <p>O limite de upload de vídeo foi alterado para <strong>20MB</strong></p>
    <p>Configurações atualizadas:</p>
    <ul>
        <li>Tamanho máximo de vídeo: 20MB</li>
        <li>Formatos aceitos: MP4, WebM</li>
        <li>Conversão automática WebM → MP4 (se FFmpeg disponível)</li>
    </ul>
    <p><a href="/test-config">Ver configurações</a></p>
    '''

@test_app.route('/test-config')
def test_config():
    try:
        from app import app as main_app
        config_info = {
            'MAX_VIDEO_SIZE': main_app.config.get('MAX_VIDEO_SIZE', 'Não definido'),
            'ALLOWED_VIDEO_EXTENSIONS': main_app.config.get('ALLOWED_VIDEO_EXTENSIONS', 'Não definido'),
            'MAX_CONTENT_LENGTH': main_app.config.get('MAX_CONTENT_LENGTH', 'Não definido'),
        }
        
        html = '<h1>Configurações do Sistema</h1><ul>'
        for key, value in config_info.items():
            if key == 'MAX_VIDEO_SIZE' and isinstance(value, int):
                value_mb = value / (1024 * 1024)
                html += f'<li><strong>{key}:</strong> {value_mb:.0f}MB ({value} bytes)</li>'
            elif key == 'MAX_CONTENT_LENGTH' and isinstance(value, int):
                value_mb = value / (1024 * 1024)
                html += f'<li><strong>{key}:</strong> {value_mb:.0f}MB ({value} bytes)</li>'
            else:
                html += f'<li><strong>{key}:</strong> {value}</li>'
        html += '</ul><p><a href="/">Voltar</a></p>'
        return html
    except Exception as e:
        return f'<h1>Erro ao carregar configurações</h1><p>{str(e)}</p><p><a href="/">Voltar</a></p>'

if __name__ == '__main__':
    print("Iniciando servidor de teste...")
    print("Acesse: http://localhost:5000")
    test_app.run(host='0.0.0.0', port=5000, debug=True)