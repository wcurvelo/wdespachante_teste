from flask import Flask, render_template, request, redirect, url_for, flash, make_response, jsonify, abort, session, g, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from flask_caching import Cache
import os
from datetime import datetime, UTC
from slugify import slugify
import uuid # Para gerar nomes de arquivo únicos
from werkzeug.utils import secure_filename
import subprocess
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
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instance', 'site.db')
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

# Garante que as tabelas do banco de dados são criadas ao iniciar a aplicação
with app.app_context():
    db.create_all()

os.makedirs(app.instance_path, exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER_IMAGES'], exist_ok=True)
# Pastas para diferentes tamanhos de imagem
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], 'thumb'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], 'medium'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], 'large'), exist_ok=True)

ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm'}
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB
FFMPEG_PATH = 'C:/ffmpeg/bin/ffmpeg.exe'  # Ajuste conforme o seu sistema
UPLOAD_FOLDER_VIDEOS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads', 'videos')
UPLOAD_FOLDER_GALLERY = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads', 'images', 'gallery') # Nova pasta para galeria
os.makedirs(UPLOAD_FOLDER_VIDEOS, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_GALLERY, exist_ok=True) # Criar pasta da galeria


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

def save_gallery_image(image_file):
    """Salva uma imagem da galeria no formato original com nome seguro."""
    if not image_file or not image_file.filename:
        return None

    try:
        filename = secure_filename(f"{uuid.uuid4()}_{image_file.filename}")
        filepath = os.path.join(UPLOAD_FOLDER_GALLERY, filename)
        image_file.save(filepath)
        return filename
    except Exception as e:
        logger.error(f"Erro ao salvar imagem da galeria: {e}")
        return None


def delete_gallery_image_file(filename):
    """Deleta um arquivo de imagem da galeria."""
    if not filename:
        return
    try:
        path = os.path.join(UPLOAD_FOLDER_GALLERY, filename)
        if os.path.exists(path):
            os.remove(path)
            logger.info(f"Imagem da galeria deletada: {filename}")
    except Exception as e:
        logger.error(f"Erro ao deletar imagem da galeria {filename}: {e}")


# --- Models Admin Views ---
class CustomAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        # Esta view agora apenas redireciona para o novo dashboard customizado.
        # A lógica de carregar estatísticas foi movida para a rota 'custom_dashboard'.
        return redirect(url_for('custom_dashboard'))

class UserAdminView(ModelView):
    column_exclude_list = ('password_hash',)
    form_excluded_columns = ('password_hash', 'news_articles', 'comments')
    form_columns = ('username', 'email', 'role', 'active')
    
    def on_model_change(self, form, model, is_created):
        if form.password.data:
            model.set_password(form.password.data)

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

# --- Custom Admin Routes ---
@app.route('/admin/dashboard')
@login_required
def custom_dashboard():
    if not current_user.is_admin:
        flash('Acesso não autorizado.', 'danger')
        return redirect(url_for('index'))

    try:
        # Estatísticas principais
        news_count = News.query.count()
        pending_comments_count = Comment.query.filter_by(approved=False).count()
        user_count = User.query.count()
        logger.info(f"Dashboard Stats - News: {news_count}, Pending Comments: {pending_comments_count}, Users: {user_count}")

        # Dados para as tabelas
        recent_news = News.query.order_by(News.publication_date.desc()).limit(5).all()
        recent_comments = Comment.query.order_by(Comment.publication_date.desc()).limit(5).all()
        logger.info(f"Dashboard Stats - Recent News Count: {len(recent_news)}, Recent Comments Count: {len(recent_comments)}")

        # Dados para o gráfico de status (exemplo)
        news_status_counts = db.session.query(News.status, func.count(News.id)).group_by(News.status).all()
        news_by_status = {status: count for status, count in news_status_counts}
        logger.info(f"Dashboard Stats - News by Status: {news_by_status}")

        stats = {
            'news': news_count,
            'pending_comments': pending_comments_count,
            'users': user_count,
            'recent_news': recent_news,
            'recent_comments': recent_comments,
            'news_by_status': news_by_status
        }
        return render_template('admin/custom_dashboard.html', stats=stats)
    except Exception as e:
        logger.error(f"Erro ao carregar o dashboard customizado: {e}")
        abort(500)


@app.route('/admin/news/new', methods=['GET', 'POST'])
@app.route('/admin/news/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def custom_news_form(id=None):
    if not current_user.is_admin:
        abort(403)

    article = News.query.get_or_404(id) if id else None

    if request.method == 'POST':
        title = request.form.get('title')
        summary = request.form.get('summary')
        content = request.form.get('content')
        status = request.form.get('status', 'draft')
        category_id = request.form.get('category')
        video_url = request.form.get('video_url', '').strip()
        video_file = request.files.get('video_upload')
        video_filename = None
        error = None
        social_share_title = request.form.get('social_share_title', '').strip()
        social_share_description = request.form.get('social_share_description', '').strip()

        # Validação: só pode um dos dois
        if video_url and video_file and video_file.filename:
            flash('Escolha apenas uma opção: URL ou upload de vídeo.', 'danger')
            return render_template('admin/custom_news_form.html', news=article, categories=Category.query.all())

        # Processar upload de vídeo
        if video_file and video_file.filename:
            ext = video_file.filename.rsplit('.', 1)[-1].lower()
            if ext not in ALLOWED_VIDEO_EXTENSIONS:
                flash('Formato de vídeo inválido. Só MP4 ou WebM.', 'danger')
                return render_template('admin/custom_news_form.html', news=article, categories=Category.query.all())
            if video_file.content_length and video_file.content_length > MAX_VIDEO_SIZE:
                flash('Arquivo de vídeo muito grande. Máx. 100MB.', 'danger')
                return render_template('admin/custom_news_form.html', news=article, categories=Category.query.all())
            # Salvar arquivo
            filename = secure_filename(f"{uuid.uuid4()}.{ext}")
            save_path = os.path.join(UPLOAD_FOLDER_VIDEOS, filename)
            video_file.save(save_path)
            # Transcodificar para MP4 se não for mp4
            if ext != 'mp4':
                mp4_filename = filename.rsplit('.', 1)[0] + '.mp4'
                mp4_path = os.path.join(UPLOAD_FOLDER_VIDEOS, mp4_filename)
                try:
                    subprocess.run([FFMPEG_PATH, '-i', save_path, '-c:v', 'libx264', '-preset', 'fast', '-crf', '23', mp4_path], check=True)
                    os.remove(save_path)
                    filename = mp4_filename
                except Exception as e:
                    flash(f'Erro ao converter vídeo: {e}', 'danger')
                    return render_template('admin/custom_news_form.html', news=article, categories=Category.query.all())
            video_filename = filename
            video_url = ''  # Limpa o campo URL
        elif video_url:
            # Validação básica de URL
            if not (video_url.startswith('https://www.youtube.com/') or video_url.startswith('https://youtu.be/') or video_url.startswith('https://vimeo.com/')):
                flash('URL de vídeo inválida. Use YouTube ou Vimeo.', 'danger')
                return render_template('admin/custom_news_form.html', news=article, categories=Category.query.all())
            video_filename = None
        else:
            video_filename = None
            video_url = ''

        if not title or not content:
            flash('Título e Conteúdo são campos obrigatórios.', 'danger')
            return render_template('admin/custom_news_form.html', news=article, categories=Category.query.all())

        # Processar Galeria de Imagens
        current_gallery_images = json.loads(article.gallery_image_filenames) if article and article.gallery_image_filenames else []
        updated_gallery_images = []

        # Remover imagens existentes que foram desmarcadas
        if request.form.get('deleted_gallery_images'):
            deleted_images_str = request.form.get('deleted_gallery_images')
            deleted_images_list = json.loads(deleted_images_str)
            for del_img in deleted_images_list:
                if del_img in current_gallery_images:
                    current_gallery_images.remove(del_img)
                    delete_gallery_image_file(del_img)

        # Adicionar imagens novas
        for file in request.files.getlist('gallery_images'):
            if file.filename == '':
                continue
            saved_filename = save_gallery_image(file)
            if saved_filename:
                updated_gallery_images.append(saved_filename)
        
        # Combinar e garantir unicidade (se houver)
        final_gallery_images = list(set(current_gallery_images + updated_gallery_images))
        gallery_image_filenames_json = json.dumps(final_gallery_images)


        if article:
            article.title = title
            article.summary = summary
            article.content = content
            article.status = status
            article.category_id = category_id
            article.publication_date = datetime.now()
            article.generate_slug()
            article.video_url = video_url
            article.video_filename = video_filename
            article.gallery_image_filenames = gallery_image_filenames_json # Salva a galeria
            article.social_share_title = social_share_title
            article.social_share_description = social_share_description
            flash('Notícia atualizada com sucesso!', 'success')
        else:
            article = News(
                title=title,
                summary=summary,
                content=content,
                status=status,
                user_id=current_user.id,
                category_id=category_id,
                video_url=video_url,
                video_filename=video_filename,
                gallery_image_filenames=gallery_image_filenames_json,
                social_share_title=social_share_title,
                social_share_description=social_share_description
            )
            article.generate_slug()
            db.session.add(article)
            flash('Notícia criada com sucesso!', 'success')

        # Processar imagem destacada
        if 'featured_image' in request.files and request.files['featured_image'].filename != '':
            image_file = request.files['featured_image']
            saved_filename = save_optimized_image(image_file, app.config['UPLOAD_FOLDER_IMAGES'])
            if saved_filename:
                if article.featured_image:
                    delete_image_file(article.featured_image)
                article.featured_image = saved_filename

        db.session.commit()
        return redirect(url_for('custom_dashboard'))

    categories = Category.query.all()
    pub_date_now = datetime.now().strftime('%Y-%m-%dT%H:%M')
    # Carregar imagens da galeria se o artigo existir
    gallery_images = json.loads(article.gallery_image_filenames) if article and article.gallery_image_filenames else []
    return render_template('admin/custom_news_form.html', news=article, categories=categories, pub_date_now=pub_date_now, gallery_images=gallery_images)


@app.route('/admin/news')
@login_required
def custom_news_list():
    if not current_user.is_admin:
        abort(403)
    
    page = request.args.get('page', 1, type=int)
    
    # Consulta base paginada
    news_pagination = News.query.order_by(News.publication_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('admin/custom_news_list.html', news_pagination=news_pagination)


def delete_image_file(filename):
    """Função auxiliar para deletar arquivos de imagem de todas as pastas."""
    if not filename:
        return
    try:
        for size in ['thumb', 'medium', 'large']:
            path = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], size, filename)
            if os.path.exists(path):
                os.remove(path)
    except Exception as e:
        logger.error(f"Erro ao deletar o arquivo de imagem {filename}: {e}")


# --- Admin Setup ---
admin = Admin(app, name='WDespachante Admin', template_mode='bootstrap4', index_view=CustomAdminIndexView(name='Dashboard', url='/admin'))

admin.add_view(UserAdminView(User, db.session, name='Usuários'))
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
    # Substituir User.query.get(int(user_id)) por db.session.get(User, int(user_id))
    # para resolver o LegacyAPIWarning do SQLAlchemy 2.0
    return db.session.get(User, int(user_id))

@app.context_processor
def inject_now():
    return {'now': datetime.now(UTC)}

# Filtro Jinja2 para desserializar JSON
@app.template_filter('from_json')
def from_json_filter(value):
    if value is None:
        return []
    return json.loads(value)

# --- Public Routes ---
@app.route('/debug-db')
def debug_db():
    try:
        db_path = app.config['SQLALCHEMY_DATABASE_URI']
        instance_path = app.instance_path
        engine_url = str(db.engine.url)
        
        debug_info = f"""
        Caminho da Instância (app.instance_path): {instance_path}
        SQLALCHEMY_DATABASE_URI: {db_path}
        Engine URL (db.engine.url): {engine_url}
        """
        logger.info(f"Informações de Debug do Banco de Dados:\n{debug_info}")
        
        # Tenta uma consulta simples para verificar a conexão
        try:
            user_count = User.query.count()
            news_count = News.query.count()
            service_count = Service.query.count()
            debug_info += f"\nContagem de Usuários: {user_count}"
            debug_info += f"\nContagem de Notícias: {news_count}"
            debug_info += f"\nContagem de Serviços: {service_count}"
            logger.info(f"Contagens do Banco de Dados:\n{debug_info}")
        except Exception as query_e:
            debug_info += f"\nErro ao realizar consulta de teste: {query_e}"
            logger.error(f"Erro na consulta de debug: {query_e}")

        return f"<pre>{debug_info}</pre>", 200
    except Exception as e:
        logger.error(f"Erro ao acessar rota de debug: {e}")
        return f"Erro ao carregar informações de debug: {e}", 500

@app.route('/')
def index():
    latest_news = News.query.order_by(News.publication_date.desc()).limit(3).all()
    # Fetch only featured services for the "Nossos Serviços" section, limited to 6
    services = Service.query.filter_by(featured=True).order_by(Service.order.asc()).limit(6).all()
    testimonials = Testimonial.query.all()
    faqs = FAQ.query.all()
    return render_template('home_new.html', latest_news=latest_news, services=services, testimonials=testimonials, faqs=faqs)

@app.route('/servicos')
def services_list():
    try:
        services = Service.query.filter_by(active=True).order_by(Service.order).all()
        logger.info(f"Serviços carregados para /servicos: {len(services)} serviços ativos.")
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
    news_pagination = News.query.filter_by(status='published').order_by(News.publication_date.desc()).paginate(page=page, per_page=10)
    categories = Category.query.all()
    recent_news = News.query.order_by(News.publication_date.desc()).limit(5).all()
    tags = Tag.query.all()
    return render_template('news/blog.html', articles=news_pagination, categories=categories, recent_news=recent_news, tags=tags)

@app.route('/blog/<slug>')
def news_detail(slug):
    news = News.query.filter_by(slug=slug, status='published').first_or_404()
    latest_news = News.query.filter(News.id != news.id, News.status=='published').order_by(News.publication_date.desc()).limit(5).all()
    return render_template('news/news_detail.html', news=news, latest_news=latest_news)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    results = News.query.filter(News.title.contains(query) | News.content.contains(query)).all()
    return render_template('search.html', results=results, query=query)
    
@app.route('/politica-de-privacidade')
def politica_privacidade():
    return render_template('politica-privacidade.html')

@app.route('/termos-de-uso')
def termos_de_uso():
    return render_template('termos-de-uso.html')

@app.route('/obrigado')
def obrigado():
    return render_template('obrigado.html')

@app.route('/links-uteis')
def links_uteis():
    links = LinkUtil.query.order_by(LinkUtil.order).all()
    return render_template('links_uteis.html', links=links)

@app.route('/detrans-do-brasil')
def detrans_do_brasil():
    detrans = Detran.query.order_by(Detran.order).all()
    return render_template('detrans_do_brasil.html', detrans=detrans)

@app.route('/test-concessionaria-image')
def test_concessionaria_image():
    return send_from_directory(app.root_path + '/static/images/', 'concessionaria.jpeg')

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
        phone = request.form.get('phone') # Campo de telefone opcional
        subject = request.form.get('subject') # Assunto é opcional, pode ser inferido ou removido se não usado
        message = request.form.get('message')

        if not name or not email or not message:
            flash('Por favor, preencha todos os campos obrigatórios.', 'danger')
            return redirect(url_for('index') + '#contact')

        contact_message = ContactMessage(
            name=name,
            email=email,
            phone=phone, # Adicionado o campo de telefone
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
    app.run(host='0.0.0.0', port=5000, debug=True)