from app import app, db
from models import News, User, Comment, Category, Tag, news_tags
from sqlalchemy import inspect, text
from slugify import slugify
import sys
import sqlite3
import os

def add_column(engine, table_name, column):
    column_name = column.split()[0]
    column_type = column.split()[1]
    
    # Verificar se a coluna já existe
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    
    if column_name not in columns:
        engine.execute(f'ALTER TABLE {table_name} ADD COLUMN {column} NULL')
        print(f"Coluna {column_name} adicionada à tabela {table_name}")
    else:
        print(f"Coluna {column_name} já existe na tabela {table_name}")
    
    return column_name in columns

def column_exists(engine, table_name, column_name):
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def migrate_categories_and_tags():
    """
    Migra as categorias e tags existentes para os novos modelos.
    """
    print("Iniciando migração de categorias e tags...")
    
    with app.app_context():
        engine = db.engine
        
        # Verificar e adicionar colunas necessárias
        if not column_exists(engine, 'news', 'category_id'):
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE news ADD COLUMN category_id INTEGER"))
                print("Coluna category_id adicionada à tabela news")
        
        if not column_exists(engine, 'news', 'author_id'):
            with engine.connect() as conn:
                conn.execute(text("ALTER TABLE news ADD COLUMN author_id INTEGER"))
                print("Coluna author_id adicionada à tabela news")
        
        # Migrar categorias
        print("Migrando categorias...")
        unique_categories = {}
        
        # Coletar categorias únicas das notícias
        for news in News.query.all():
            if news.category and news.category.strip():
                category_name = news.category.strip()
                if category_name not in unique_categories:
                    unique_categories[category_name] = None
        
        # Criar objetos de categoria para cada categoria única
        for category_name in unique_categories:
            existing_category = Category.query.filter_by(name=category_name).first()
            if not existing_category:
                slug = slugify(category_name)
                base_slug = slug
                counter = 1
                while Category.query.filter_by(slug=slug).first():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                new_category = Category(name=category_name, slug=slug)
                db.session.add(new_category)
                unique_categories[category_name] = new_category
        
        # Commit para salvar as categorias antes de associá-las às notícias
        db.session.commit()
        
        # Associar notícias às categorias
        print("Associando notícias às categorias...")
        for news in News.query.all():
            if news.category and news.category.strip():
                category_name = news.category.strip()
                category = Category.query.filter_by(name=category_name).first()
                if category:
                    news.category_id = category.id
        
        # Migrar tags
        print("Migrando tags...")
        unique_tags = {}
        
        # Coletar tags únicas das notícias
        for news in News.query.all():
            if news.tags and news.tags.strip():
                tag_list = [tag.strip() for tag in news.tags.split(',') if tag.strip()]
                for tag_name in tag_list:
                    if tag_name not in unique_tags:
                        unique_tags[tag_name] = None
        
        # Criar objetos de tag para cada tag única
        for tag_name in unique_tags:
            existing_tag = Tag.query.filter_by(name=tag_name).first()
            if not existing_tag:
                slug = slugify(tag_name)
                base_slug = slug
                counter = 1
                while Tag.query.filter_by(slug=slug).first():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                
                new_tag = Tag(name=tag_name, slug=slug)
                db.session.add(new_tag)
                unique_tags[tag_name] = new_tag
        
        # Commit para salvar as tags antes de associá-las às notícias
        db.session.commit()
        
        # Associar notícias às tags através da tabela de associação
        print("Associando notícias às tags...")
        for news in News.query.all():
            if news.tags and news.tags.strip():
                tag_list = [tag.strip() for tag in news.tags.split(',') if tag.strip()]
                for tag_name in tag_list:
                    tag = Tag.query.filter_by(name=tag_name).first()
                    if tag and tag not in news.tags_rel:
                        news.tags_rel.append(tag)
        
        # Commit final
        db.session.commit()
        
        print("Migração concluída com sucesso!")
        print(f"Total de categorias criadas: {Category.query.count()}")
        print(f"Total de tags criadas: {Tag.query.count()}")

def add_column_if_not_exists(conn, table, column, column_type):
    """Adiciona uma coluna se ela não existir na tabela"""
    cursor = conn.cursor()
    # Verificar se a coluna existe
    cursor.execute(f"PRAGMA table_info({table})")
    columns = [info[1] for info in cursor.fetchall()]
    
    if column not in columns:
        print(f"Adicionando coluna '{column}' à tabela '{table}'...")
        cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")
        print(f"Coluna '{column}' adicionada com sucesso!")
    else:
        print(f"Coluna '{column}' já existe na tabela '{table}'")

# Caminho para o banco de dados
db_path = os.path.join(app.instance_path, 'site.db')

# Conectar ao banco de dados SQLite diretamente
conn = sqlite3.connect(db_path)

try:
    # Adicionar colunas faltantes à tabela news
    colunas = [
        ('summary', 'TEXT'),
        ('meta_description', 'TEXT'),
        ('featured_image', 'TEXT'),
        ('gallery_images', 'TEXT'),
        ('video_filename', 'TEXT'),
        ('video_embed_url', 'TEXT'),
        ('video_url', 'TEXT'),
        ('sources', 'TEXT'),
        ('is_featured', 'BOOLEAN'),
        ('social_title', 'TEXT'),
        ('social_description', 'TEXT')
    ]
    
    for coluna, tipo in colunas:
        add_column_if_not_exists(conn, 'news', coluna, tipo)
    
    print("Atualização do banco de dados concluída!")
    
except Exception as e:
    print(f"Erro durante a atualização do banco de dados: {e}")
finally:
    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--confirm":
        migrate_categories_and_tags()
    else:
        print("ATENÇÃO: Este script irá migrar as categorias e tags existentes para os novos modelos.")
        print("Certifique-se de ter feito backup do banco de dados antes de continuar.")
        print("Para confirmar a execução, execute o script com o parâmetro --confirm:")
        print("python update_db.py --confirm") 