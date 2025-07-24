from app import app, db, News, Category, Tag

def check_db():
    with app.app_context():
        print("\nVerificando notícias:")
        news = News.query.all()
        for n in news:
            print(f"\nNotícia ID: {n.id}")
            print(f"Título: {n.title}")
            print(f"Slug: {n.slug}")
            print(f"Autor: {n.author}")
            print(f"Categoria ID: {n.category_id}")
            print(f"Status: {n.status}")
            if n.tags_rel:
                print("Tags:", ", ".join([t.name for t in n.tags_rel]))
            
        print("\nVerificando categorias:")
        categories = Category.query.all()
        for c in categories:
            print(f"\nCategoria ID: {c.id}")
            print(f"Nome: {c.name}")
            print(f"Slug: {c.slug}")
            
        print("\nVerificando tags:")
        tags = Tag.query.all()
        for t in tags:
            print(f"\nTag ID: {t.id}")
            print(f"Nome: {t.name}")
            print(f"Slug: {t.slug}")

if __name__ == '__main__':
    check_db() 