import os
import glob

def remove_bom_and_fix_encoding(file_path):
    """Remove BOM e corrige encoding do arquivo"""
    try:
        # Tentar ler com diferentes encodings
        content = None
        detected_encoding = None
        
        for encoding in ['utf-8-sig', 'utf-8', 'utf-16', 'latin-1', 'cp1252']:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                detected_encoding = encoding
                break
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        if content is not None:
            # Remover BOM se existir
            if content.startswith('\ufeff'):
                content = content[1:]
            
            # Reescrever em UTF-8 limpo
            with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(content)
            
            print(f"✅ {file_path} - Corrigido (era {detected_encoding})")
            return True
        else:
            print(f"❌ {file_path} - Não foi possível ler")
            return False
            
    except Exception as e:
        print(f"❌ {file_path} - Erro: {e}")
        return False

def fix_all_templates():
    """Corrigir encoding de todos os templates"""
    
    # Encontrar todos os arquivos HTML
    html_files = []
    for root, dirs, files in os.walk('templates'):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    
    print(f"Encontrados {len(html_files)} arquivos HTML para corrigir...\n")
    
    success_count = 0
    for file_path in html_files:
        if remove_bom_and_fix_encoding(file_path):
            success_count += 1
    
    print(f"\n✅ {success_count}/{len(html_files)} arquivos corrigidos com sucesso!")
    
    # Verificar arquivos específicos que estavam causando problemas
    problem_files = [
        'templates/error.html',
        'templates/base.html',
        'templates/news/news_detail.html',
        'templates/news/blog.html'
    ]
    
    print("\n🔍 Verificando arquivos problemáticos específicos:")
    for file_path in problem_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                print(f"✅ {file_path} - Legível em UTF-8")
            except UnicodeDecodeError as e:
                print(f"❌ {file_path} - Ainda com problema: {e}")
        else:
            print(f"⚠️ {file_path} - Arquivo não encontrado")

if __name__ == "__main__":
    print("🔧 Corrigindo encoding de todos os templates...\n")
    fix_all_templates()
    print("\n✨ Processo concluído! Reinicie o servidor.") 