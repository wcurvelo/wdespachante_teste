import os
import sys
from app import app, db
from models import News

def fix_template_encoding():
    """Corrigir problemas de encoding nos templates"""
    
    template_files = [
        'templates/base.html',
        'templates/news/news_detail.html',
        'templates/news/blog.html'
    ]
    
    for template_path in template_files:
        if os.path.exists(template_path):
            try:
                # Tentar ler o arquivo em diferentes encodings
                content = None
                for encoding in ['utf-8', 'utf-16', 'latin-1', 'cp1252']:
                    try:
                        with open(template_path, 'r', encoding=encoding) as f:
                            content = f.read()
                        print(f"✅ {template_path} lido com encoding: {encoding}")
                        break
                    except UnicodeDecodeError:
                        continue
                
                if content:
                    # Reescrever o arquivo em UTF-8
                    with open(template_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ {template_path} reescrito em UTF-8")
                else:
                    print(f"❌ Não foi possível ler {template_path}")
                    
            except Exception as e:
                print(f"❌ Erro ao processar {template_path}: {e}")

def fix_database_encoding():
    """Corrigir problemas de encoding nos dados do banco"""
    
    with app.app_context():
        articles = News.query.all()
        
        for article in articles:
            try:
                # Verificar e corrigir encoding nos campos de texto
                if article.title:
                    article.title = article.title.encode('utf-8', errors='ignore').decode('utf-8')
                
                if article.content:
                    article.content = article.content.encode('utf-8', errors='ignore').decode('utf-8')
                
                if article.meta_description:
                    article.meta_description = article.meta_description.encode('utf-8', errors='ignore').decode('utf-8')
                
                if article.tags:
                    article.tags = article.tags.encode('utf-8', errors='ignore').decode('utf-8')
                
                print(f"✅ Encoding corrigido para: {article.title[:50]}...")
                
            except Exception as e:
                print(f"❌ Erro ao corrigir encoding do artigo {article.id}: {e}")
        
        try:
            db.session.commit()
            print("✅ Alterações salvas no banco de dados")
        except Exception as e:
            print(f"❌ Erro ao salvar no banco: {e}")
            db.session.rollback()

def create_safe_error_template():
    """Criar um template de erro seguro"""
    
    error_content = '''<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Erro - Wellington Despachante RJ</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f5f5f5;
            margin: 0;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }
        .error-container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
            text-align: center;
            max-width: 500px;
        }
        .error-icon {
            font-size: 4rem;
            color: #e74c3c;
            margin-bottom: 20px;
        }
        h1 {
            color: #2c3e50;
            margin-bottom: 20px;
        }
        p {
            color: #7f8c8d;
            line-height: 1.6;
            margin-bottom: 30px;
        }
        .btn {
            background: #3498db;
            color: white;
            padding: 12px 24px;
            text-decoration: none;
            border-radius: 5px;
            display: inline-block;
            transition: background 0.3s;
        }
        .btn:hover {
            background: #2980b9;
        }
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-icon">⚠️</div>
        <h1>Oops! Algo deu errado</h1>
        <p>Encontramos um problema temporário. Nossa equipe já foi notificada e está trabalhando para resolver.</p>
        <a href="/" class="btn">Voltar ao Início</a>
    </div>
</body>
</html>'''
    
    with open('templates/error_safe.html', 'w', encoding='utf-8') as f:
        f.write(error_content)
    
    print("✅ Template de erro seguro criado")

if __name__ == "__main__":
    print("🔧 Corrigindo problemas de encoding...\n")
    
    print("1. Corrigindo templates...")
    fix_template_encoding()
    
    print("\n2. Corrigindo dados do banco...")
    fix_database_encoding()
    
    print("\n3. Criando template de erro seguro...")
    create_safe_error_template()
    
    print("\n✅ Correções concluídas! Reinicie o servidor.") 