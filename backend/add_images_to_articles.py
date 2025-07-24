from app import app, db
from models import News
import os
import shutil

def create_placeholder_images():
    """Criar imagens placeholder para os artigos"""
    
    # Definir imagens para cada tipo de artigo
    article_images = {
        'transferencia': 'transferencia_veiculo.jpg',
        'cnh': 'renovacao_cnh.jpg', 
        'ipva': 'ipva_2025.jpg',
        'vistoria': 'vistoria_veicular.jpg',
        'producao': 'producao_carros.jpg',
        'isencao': 'isencao_impostos.jpg'
    }
    
    # Criar diretórios se não existirem
    directories = [
        'static/uploads/images/original',
        'static/uploads/images/medium', 
        'static/uploads/images/thumb'
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Diretório criado: {directory}")
    
    # Criar arquivos de imagem placeholder (texto informativo)
    placeholder_content = """
    Esta é uma imagem placeholder.
    
    Para usar imagens reais:
    1. Substitua este arquivo por uma imagem JPG/PNG
    2. Mantenha o mesmo nome do arquivo
    3. Recomendado: 1200x630px para original, 800x400px para medium, 300x200px para thumb
    
    Imagem: {}
    """
    
    for image_type, filename in article_images.items():
        for size in ['original', 'medium', 'thumb']:
            filepath = f'static/uploads/images/{size}/{filename}'
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(placeholder_content.format(f"{image_type}_{size}"))
            
            print(f"✅ Placeholder criado: {filepath}")

def assign_images_to_articles():
    """Associar imagens aos artigos existentes"""
    
    with app.app_context():
        # Mapear artigos para imagens
        article_image_mapping = {
            'como-fazer-transferencia-propriedade-veiculo-rj': 'transferencia_veiculo.jpg',
            'renovacao-cnh-tudo-que-precisa-saber': 'renovacao_cnh.jpg',
            'ipva-2024-calendario-vencimentos-como-pagar': 'ipva_2025.jpg',
            'vistoria-veicular-quando-obrigatoria-como-fazer': 'vistoria_veicular.jpg'
        }
        
        # Buscar artigos por slug e adicionar imagens
        for slug, image_filename in article_image_mapping.items():
            article = News.query.filter_by(slug=slug).first()
            if article:
                article.featured_image = image_filename
                print(f"✅ Imagem adicionada ao artigo: {article.title[:50]}...")
        
        # Adicionar imagens aos outros artigos por título
        title_image_mapping = {
            'Produção de Carros': 'producao_carros.jpg',
            'Isenção de Impostos': 'isencao_impostos.jpg',
            'IPVA 2025': 'ipva_2025.jpg'
        }
        
        for title_part, image_filename in title_image_mapping.items():
            articles = News.query.filter(News.title.contains(title_part)).all()
            for article in articles:
                if not article.featured_image:  # Só adicionar se não tiver imagem
                    article.featured_image = image_filename
                    print(f"✅ Imagem adicionada ao artigo: {article.title[:50]}...")
        
        # Salvar alterações
        db.session.commit()
        print("\n🎉 Todas as imagens foram associadas aos artigos!")

if __name__ == "__main__":
    print("🖼️ Criando imagens placeholder e associando aos artigos...\n")
    create_placeholder_images()
    print("\n" + "="*50)
    assign_images_to_articles()
    print("\n✨ Processo concluído! Agora todos os artigos têm imagens.") 