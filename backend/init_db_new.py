from app import app, db, User, News, Category, Tag, bcrypt
from datetime import datetime

def init_db():
    with app.app_context():
        # Criar tabelas
        db.create_all()
        
        # Criar usuário admin se não existir
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                role='admin',
                active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Usuário admin criado!")
        
        # Criar categoria de teste
        category = Category.query.filter_by(name='Noticias').first()
        if not category:
            category = Category(
                name='Noticias',
                description='Noticias e atualizacoes',
                slug='noticias'  # Adicionando slug explicitamente
            )
            db.session.add(category)
            db.session.commit()
            print("Categoria criada!")
        
        # Criar tag de teste
        tag = Tag.query.filter_by(name='Detran').first()
        if not tag:
            tag = Tag(
                name='Detran',
                slug='detran'  # Adicionando slug explicitamente
            )
            db.session.add(tag)
            db.session.commit()
            print("Tag criada!")
        
        # Criar notícia de teste
        test_news = News.query.filter_by(title='Novidades do Detran RJ').first()
        if not test_news:
            test_news = News(
                title='Novidades do Detran RJ',
                content='<p>O Detran RJ anunciou novas medidas para facilitar o atendimento aos cidadãos. Entre as principais mudanças estão:</p><ul><li>Agendamento online para todos os serviços</li><li>Ampliação do horário de atendimento</li><li>Novo sistema de chamada por SMS</li></ul><p>As medidas começam a valer a partir do próximo mês e visam reduzir o tempo de espera e melhorar a qualidade do atendimento.</p>',
                author='Admin',
                author_id=admin.id,
                category_id=category.id,
                category=category.name,  # Adicionando nome da categoria
                status='published',
                meta_description='Confira as últimas novidades e mudanças no Detran RJ para melhorar o atendimento aos cidadãos',
                publication_date=datetime.now(),
                allow_comments=True,
                is_featured=True,
                tags='detran,atendimento,novidades'  # Adicionando tags como string
            )
            
            # Adicionar a tag à notícia
            test_news.tags_rel.append(tag)
            
            # Gerar slug manualmente
            from slugify import slugify
            test_news.slug = slugify(test_news.title)
            
            db.session.add(test_news)
            db.session.commit()
            print("Notícia de teste criada!")
            print(f"Acesse em: /blog/{test_news.slug}")
            
            # Verificar se a notícia foi criada corretamente
            created_news = News.query.get(test_news.id)
            print("\nDetalhes da notícia criada:")
            print(f"ID: {created_news.id}")
            print(f"Título: {created_news.title}")
            print(f"Slug: {created_news.slug}")
            print(f"Categoria: {created_news.category} (ID: {created_news.category_id})")
            print(f"Tags: {created_news.tags}")
            print(f"Tags relacionadas: {[t.name for t in created_news.tags_rel]}")
            print(f"Status: {created_news.status}")

if __name__ == '__main__':
    print("Inicializando banco de dados...")
    init_db()
    print("Banco de dados inicializado com sucesso!") 