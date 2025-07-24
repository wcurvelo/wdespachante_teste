from app import app, db, User
from sqlalchemy import exc

def initialize_database():
    """
    Apaga e recria o banco de dados e o usuário admin.
    """
    with app.app_context():
        print("--- Iniciando a inicialização do banco de dados ---")
        
        try:
            print("Apagando tabelas existentes (se houver)...")
            db.drop_all()
            print("Tabelas apagadas.")
        except exc.SQLAlchemyError as e:
            print(f"Nenhuma tabela para apagar ou ocorreu um erro: {e}")

        try:
            print("Criando novas tabelas a partir dos modelos...")
            db.create_all()
            print("Novas tabelas criadas com sucesso.")
        except exc.SQLAlchemyError as e:
            print(f"ERRO: Não foi possível criar as tabelas: {e}")
            return

        # Criar usuário admin se ele não existir
        if not User.query.filter_by(username='admin').first():
            print("Criando usuário 'admin' padrão...")
            try:
                admin_user = User(username='admin', role='admin')
                admin_user.set_password('admin') # Senha é 'admin'
                db.session.add(admin_user)
                db.session.commit()
                print("Usuário 'admin' criado com sucesso.")
            except exc.SQLAlchemyError as e:
                print(f"ERRO: Não foi possível criar o usuário admin: {e}")
                db.session.rollback()
        else:
            print("Usuário 'admin' já existe. Nenhuma ação necessária.")
            
        print("--- Inicialização do banco de dados concluída ---")

if __name__ == '__main__':
    initialize_database()
