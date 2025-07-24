from app import app, db

def clear_db():
    with app.app_context():
        # Remover todas as tabelas
        db.drop_all()
        print("Banco de dados limpo com sucesso!")

if __name__ == '__main__':
    print("Limpando banco de dados...")
    clear_db() 