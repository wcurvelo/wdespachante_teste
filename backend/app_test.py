from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import os
from datetime import datetime, timedelta
import json

app = Flask(__name__, instance_path=os.path.abspath(os.path.join(os.path.dirname(__file__), 'instance')))
app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_segura_e_longa_que_deve_ser_substituida_em_producao'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Garantir que o diretório instance existe
os.makedirs(app.instance_path, exist_ok=True)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), default='editor')
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.username}>'

    def is_active(self):
        return self.active

    def is_admin(self):
        return self.role == 'admin'
        
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
        
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

# Função para criar tabelas e usuário admin
def create_tables():
    with app.app_context():
        db.create_all()
        # Verificar se já existe um usuário admin
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
            print("Usuário admin criado com sucesso!")

# Criar tabelas e usuário admin
create_tables()

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def index():
    return "Bem-vindo ao site! Em breve, suas notícias aqui."

@app.route('/admin')
@login_required
def admin_dashboard():
    # Estatísticas para o dashboard
    # Data atual
    current_date = datetime.now()
    day_delta = timedelta(days=1)
    
    # Total de notícias
    total_news = 0  # Placeholder
    
    # Comentários pendentes
    pending_comments = 0  # Placeholder

    # Comentários recentes
    recent_comments = []  # Placeholder

    # Usuários
    total_users = User.query.filter_by(active=True).count()
    
    # Visualizações
    views_today = 100  # Placeholder - implementar tracking de visualizações
    views_trend = 5    # Placeholder - percentual de aumento/diminuição
    
    # Visualizações dos últimos 7 dias (placeholder)
    views_last_7_days = [45, 62, 78, 70, 85, 90, 100]
    
    # Formatar datas para o gráfico
    view_dates = []
    for i in range(6, -1, -1):
        date = (current_date - (day_delta * i)).strftime("%d/%m")
        view_dates.append(date)
    
    # Notícias por status
    news_by_status = {
        'published': 0,
        'draft': 0,
        'scheduled': 0
    }
    
    # Notícias por categoria
    category_labels = ["Notícias", "Tecnologia", "Esportes", "Cultura"]
    category_counts = [5, 3, 2, 1]
    
    # Compilar todas as estatísticas em um único objeto
    stats = {
        'current_date': current_date,
        'total_news': total_news,
        'pending_comments': pending_comments,
        'recent_comments': recent_comments,
        'total_users': total_users,
        'views_today': views_today,
        'views_trend': views_trend,
        'views_last_7_days': json.dumps(views_last_7_days),
        'view_dates': json.dumps(view_dates),
        'news_by_status': news_by_status,
        'category_labels': json.dumps(category_labels),
        'category_counts': json.dumps(category_counts)
    }
    
    # Notícias recentes
    recent_news = []  # Placeholder
    
    return render_template('admin/dashboard.html', stats=stats, recent_news=recent_news)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login realizado com sucesso!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('admin_dashboard'))
        else:
            flash('Nome de usuário ou senha incorretos. Tente novamente.', 'danger')
    
    return render_template('admin/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('index'))

@app.route('/admin/news')
@login_required
def news_list():
    return render_template('admin/news_list.html', 
                          articles=[],
                          news_pagination=None, 
                          categories=[], 
                          unique_categories=[],
                          tags=[],
                          status_filter=None,
                          category_filter=None,
                          tag_filter=None,
                          search_query=None)

@app.route('/admin/news/new', methods=['GET', 'POST'])
@login_required
def new_news_article():
    if request.method == 'POST':
        flash('Funcionalidade em desenvolvimento', 'info')
        return redirect(url_for('news_list'))
    return render_template('admin/news_form.html')

@app.route('/admin/scheduled')
@login_required
def scheduled_news():
    return render_template('admin/scheduled_news.html', scheduled_articles=[])

@app.route('/admin/categories')
@login_required
def categories_list():
    return render_template('admin/categories_list.html', categories=[])

@app.route('/admin/tags')
@login_required
def tags_list():
    return render_template('admin/tags_list.html', tags=[])

@app.route('/admin/comments')
@login_required
def comments_list():
    return render_template('admin/comments_list.html', 
                          comments=None, 
                          status_filter=None,
                          search_query=None,
                          approved_count=0,
                          pending_count=0)

@app.route('/admin/users')
@login_required
def users_list():
    if current_user.role != 'admin':
        flash('Permissão negada', 'danger')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/users_list.html', users=User.query.all())

@app.route('/admin/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        flash('Perfil atualizado com sucesso!', 'success')
        return redirect(url_for('profile'))
    return render_template('admin/profile.html')

if __name__ == '__main__':
    app.run(debug=True) 