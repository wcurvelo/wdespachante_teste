from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify, abort, session, g, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_caching import Cache
import os
from datetime import datetime
from slugify import slugify
import uuid # Para gerar nomes de arquivo únicos
from werkzeug.utils import secure_filename
from models import db, User, News, Comment, Category, Tag, NewsImage, Service, Testimonial, FAQ, ContactMessage, Detran, LinkUtil # Importar os modelos
from PIL import Image
import random
import json
from sqlalchemy import func
import logging
from flask_compress import Compress # Para compressão de resposta HTTP
from werkzeug.exceptions import NotFound

# Importações corrigidas do Flask-Admin
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from flask_ckeditor import CKEditorField

# Configurar o nível de log do Werkzeug para reduzir a verbosidade
logging.getLogger('werkzeug').setLevel(logging.WARNING)

# Configuração de logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__, instance_relative_config=True)

# Configurações do aplicativo
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER_IMAGES'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads', 'images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB

# Cache
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300
cache = Cache(app)

# Compressão
compress = Compress(app)

# Inicializar extensões
db.init_app(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Por favor, faça login para acessar esta página.'
login_manager.login_message_category = 'info'

os.makedirs(app.instance_path, exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER_IMAGES'], exist_ok=True)
# Pastas para diferentes tamanhos de imagem
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], 'thumb'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], 'medium'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], 'large'), exist_ok=True)


def save_optimized_image(image_file, output_folder):
    """Salva e otimiza uma imagem em formato WebP em vários tamanhos."""
    if not image_file or not image_file.filename:
        return None

    filename_base = str(uuid.uuid4())
    filename_webp = f"{filename_base}.webp"

    try:
        img = Image.open(image_file.stream).convert("RGB")

        # Salvar em diferentes tamanhos
        sizes = {
            'large': (1200, 800),
            'medium': (800, 600),
            'thumb': (400, 300)
        }

        for size_name, dimensions in sizes.items():
            img_copy = img.copy()
            img_copy.thumbnail(dimensions, Image.Resampling.LANCZOS)
            
            size_folder = os.path.join(output_folder, size_name)
            os.makedirs(size_folder, exist_ok=True) # Garante que a pasta de tamanho existe
            
            img_copy.save(os.path.join(size_folder, filename_webp), 'webp', quality=85)
            
        return filename_webp

    except Exception as e:
        logger.error(f"Erro ao otimizar imagem: {e}")
        return None

# --- Models Admin Views ---
class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        if not current_user.is_authenticated or not current_user.is_admin:
            return redirect(url_for('login'))
        
        # Contagens para o dashboard
        stats = {
            'services': Service.query.count(),
            'testimonials': Testimonial.query.count(),
            'faqs': FAQ.query.count(),
            'news': News.query.count(),
            'links': LinkUtil.query.count(),
            'detrans': Detran.query.count()
        }
        return self.render('admin/dashboard_new.html', stats=stats)

class UserAdminView(ModelView):
    column_exclude_list = ('password_hash',)
    form_excluded_columns = ('password_hash', 'news_articles', 'comments')
    form_columns = ('username', 'email', 'role', 'active')
    
    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.set_password(form.password.data)

class NewsAdminView(ModelView):
    form_overrides = {
        'content': CKEditorField,
        'summary': CKEditorField(description="Resumo curto para exibição em listas.")
    }
    create_template = 'admin/edit.html'
    edit_template = 'admin/edit.html'
    column_list = ('title', 'category_rel', 'author_user', 'pub_date', 'status')
    column_filters = ('status', 'category_rel.name')
    
    def on_model_change(self, form, model, is_created):
        # Gerar slug se estiver criando ou se o título for alterado
        if is_created or model.title != form.title.data:
            model.generate_slug()

        # Otimizar e salvar a imagem destacada
        if form.image.data:
            # Remover imagem antiga se existir
            if model.featured_image:
                self.delete_image(model.featured_image)
            
            # Salvar nova imagem otimizada
            model.featured_image = save_optimized_image(form.image.data, app.config['UPLOAD_FOLDER_IMAGES'])

    def on_model_delete(self, model):
        # Deletar imagem quando a notícia for excluída
        if model.featured_image:
            self.delete_image(model.featured_image)

    def delete_image(self, filename):
        """Deleta uma imagem de todas as pastas de tamanho."""
        try:
            for size in ['thumb', 'medium', 'large']:
                path = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], size, filename)
                if os.path.exists(path):
                    os.remove(path)
        except Exception as e:
            logger.error(f"Erro ao deletar imagem {filename}: {e}")


class ServiceAdminView(ModelView):
    form_overrides = {'content': CKEditorField}
    create_template = 'admin/edit.html'
    edit_template = 'admin/edit.html'
    column_list = ('name', 'summary', 'active', 'featured', 'order')
    column_filters = ('active', 'featured')
    column_editable_list = ('active', 'featured', 'order')

class TestimonialAdminView(ModelView):
    column_list = ('name', 'location', 'rating', 'featured', 'order')
    column_filters = ('featured', 'rating')
    column_editable_list = ('rating', 'featured', 'order')

class FAQAdminView(ModelView):
    column_list = ('question', 'category', 'featured', 'order')
    column_filters = ('featured', 'category')
    column_editable_list = ('featured', 'order', 'category')

class LinkUtilAdminView(ModelView):
    column_list = ('title', 'category', 'order')
    column_filters = ('category',)
    column_editable_list = ('category', 'order')

class DetranAdminView(ModelView):
    column_list = ('state', 'name', 'region')
    column_filters = ('region',)
    column_sortable_list = ('state', 'region')

# --- Admin Setup ---
admin = Admin(app, name='WDespachante Admin', template_mode='bootstrap4', index_view=CustomAdminIndexView(name='Dashboard', url='/admin'))

admin.add_view(UserAdminView(User, db.session, name='Usuários'))
admin.add_view(NewsAdminView(News, db.session, name='Notícias'))
admin.add_view(ModelView(Category, db.session, name='Categorias'))
admin.add_view(ModelView(Tag, db.session, name='Tags'))
admin.add_view(ModelView(Comment, db.session, name='Comentários'))
admin.add_view(ServiceAdminView(Service, db.session, name='Serviços'))
admin.add_view(TestimonialAdminView(Testimonial, db.session, name='Depoimentos'))
admin.add_view(FAQAdminView(FAQ, db.session, name='FAQs'))
admin.add_view(LinkUtilAdminView(LinkUtil, db.session, name='Links Úteis'))
admin.add_view(DetranAdminView(Detran, db.session, name='Detrans'))


# --- User Loader ---
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# --- Public Routes ---
@app.route('/')
def index():
    try:
        services = Service.query.filter_by(active=True, featured=True).order_by(Service.order).limit(6).all()
        testimonials = Testimonial.query.filter_by(featured=True).order_by(Testimonial.order).all()
        faqs = FAQ.query.order_by(FAQ.order).limit(5).all()
        latest_news = News.query.order_by(News.pub_date.desc()).limit(3).all()
    except Exception as e:
        logger.error(f"Erro ao buscar dados para a homepage: {e}")
        services, testimonials, faqs, latest_news = [], [], [], []
    return render_template('home_new.html', services=services, testimonials=testimonials, faqs=faqs, latest_news=latest_news)

@app.route('/servicos')
def services_list():
    try:
        services = Service.query.filter_by(active=True).order_by(Service.order).all()
        return render_template('services/services_list.html', services=services)
    except Exception as e:
        logger.error(f"Erro ao carregar a lista de serviços: {e}")
        abort(500)

@app.route('/servico/<slug>')
def service_detail(slug):
    try:
        service = Service.query.filter_by(slug=slug, active=True).first_or_404()
        related_services = Service.query.filter(Service.id != service.id, Service.active==True).order_by(func.random()).limit(3).all()
        return render_template('services/service_detail.html', service=service, related_services=related_services)
    except Exception as e:
        logger.error(f"Erro ao carregar o serviço {slug}: {e}")
        abort(404)

@app.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    news_pagination = News.query.filter_by(status='published').order_by(News.pub_date.desc()).paginate(page=page, per_page=10)
    return render_template('blog.html', news_pagination=news_pagination)

@app.route('/blog/<slug>')
def news_detail(slug):
    news = News.query.filter_by(slug=slug, status='published').first_or_404()
    return render_template('news_detail.html', news=news)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = News.query.filter(News.title.contains(query) | News.content.contains(query)).all()
    return render_template('search.html', results=results, query=query)
    
@app.route('/politica-de-privacidade')
def politica_privacidade():
    return render_template('politica-privacidade.html')

@app.route('/obrigado')
def obrigado():
    return render_template('obrigado.html')

@app.route('/robots.txt')
def robots_txt():
    return render_template('robots.txt')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.index'))
        else:
            flash('Login inválido.', 'danger')
    return render_template('admin/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/contact', methods=['POST'])
def handle_contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')

        if not name or not email or not message:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('index') + '#contact')

        contact_message = ContactMessage(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        db.session.add(contact_message)
        db.session.commit()
        
        flash('Sua mensagem foi enviada com sucesso! Entraremos em contato em breve.', 'success')
        return redirect(url_for('obrigado'))

# --- Error Handlers ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.error(f"Erro interno do servidor: {e}")
    return render_template('500.html'), 500

# --- CLI Command to Create Admin ---
@app.cli.command("create-admin")
def create_admin():
    """Cria o usuário administrador padrão."""
    if User.query.filter_by(username='admin').first():
        print("Usuário 'admin' já existe.")
        return
    
    password = 'admin' # Defina uma senha padrão segura
    user = User(username='admin', role='admin', active=True)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    print("Usuário 'admin' criado com sucesso.")
    print(f"Senha: {password}")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            create_admin()
    app.run(host='0.0.0.0', port=5000, debug=True)