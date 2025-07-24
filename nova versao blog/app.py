from flask import Flask, render_template, request, redirect, url_for, flash, make_response, send_from_directory, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
import os
from datetime import datetime
from slugify import slugify
import uuid # Para gerar nomes de arquivo únicos
from werkzeug.utils import secure_filename # Para uploads seguros
from models import db, User, News, Comment # Importar os modelos
from PIL import Image # Importar Pillow

app = Flask(__name__, instance_path=os.path.abspath(os.path.join(os.path.dirname(__file__), 'instance')))
app.config['SECRET_KEY'] = 'uma_chave_secreta_muito_segura_e_longa_que_deve_ser_substituida_em_producao'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'site.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER_IMAGES'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads', 'images')
app.config['UPLOAD_FOLDER_VIDEOS'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads', 'videos')
app.config['MAX_CONTENT_LENGTH'] = 300 * 1024 * 1024 # Limite de 300MB para uploads de imagens/vídeos
app.config['CKEDITOR_PKG_TYPE'] = 'full'
app.config['UPLOAD_FOLDER'] = 'uploads'

# Criar diretórios de upload se não existirem
os.makedirs(app.config['UPLOAD_FOLDER_IMAGES'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER_VIDEOS'], exist_ok=True)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Subpastas para imagens redimensionadas
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], 'thumb'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], 'medium'), exist_ok=True)
os.makedirs(os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], 'original'), exist_ok=True)

db.init_app(app) # Inicializar o SQLAlchemy com o app
bcrypt = Bcrypt(app) # Inicializar o Flask-Bcrypt com o app
login_manager = LoginManager(app)
login_manager.login_view = 'login' # The view to redirect to when a user needs to log in.

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'mov', 'avi', 'webm'}

@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

def allowed_file(filename, allowed_extensions):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_and_resize_image(image_file):
    if image_file and allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
        filename = str(uuid.uuid4()) + '.' + image_file.filename.rsplit('.', 1)[1].lower() # Gerar nome único e manter extensão original
        original_path = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], 'original', filename)
        thumb_path = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], 'thumb', filename)
        medium_path = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], 'medium', filename)

        # Salvar a imagem original
        image_file.save(original_path)

        img = Image.open(original_path)

        # Redimensionar para thumb (300px de largura mantendo proporção)
        img_thumb = img.copy() # Criar uma cópia para redimensionar
        img_thumb.thumbnail((300, 300))
        img_thumb.save(thumb_path)

        # Redimensionar para medium (600px de largura mantendo proporção)
        img_medium = img.copy() # Criar outra cópia da original
        img_medium.thumbnail((600, 600))
        img_medium.save(medium_path)

        return filename
    return None

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Adiciona o processador de contexto para injetar 'now' em todos os templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# --- Database Models ---
# REMOVED: User and NewsArticle model definitions are now in backend/models.py

# --- Routes ---
@app.route('/')
def home_new():
    return "Bem-vindo ao site! Em breve, suas notícias aqui."

@app.route('/blog')
def blog():
    page = request.args.get('page', 1, type=int)
    per_page = 5  # Número de artigos por página
    articles = News.query.order_by(News.publication_date.desc()).paginate(page=page, per_page=per_page)
    return render_template('news/blog.html', news_articles=articles.items, pagination=articles)

@app.route('/blog/<slug>')
def news_detail(slug):
    article = News.query.filter_by(slug=slug).first_or_404()
    # Obter apenas comentários aprovados para exibição pública
    approved_comments = Comment.query.filter_by(news_article_id=article.id, approved=True).order_by(Comment.publication_date.asc()).all()
    return render_template('news/news_detail.html', article=article, approved_comments=approved_comments)

@app.route('/blog/<int:article_id>/comment', methods=['POST'])
def add_comment(article_id):
    article = News.query.get_or_404(article_id)
    author = request.form['author']
    email = request.form.get('email')
    content = request.form['content']

    if not author or not content:
        flash('Por favor, preencha todos os campos obrigatórios (Nome e Comentário).', 'danger')
        return redirect(url_for('news_detail', slug=article.slug))

    new_comment = Comment(news_article_id=article.id, author=author,
                            email=email, content=content, approved=False)
    db.session.add(new_comment)
    db.session.commit()
    flash('Seu comentário foi enviado e está aguardando aprovação.', 'success')
    return redirect(url_for('news_detail', slug=article.slug))

@app.route('/sitemap.xml')
def sitemap():
    articles = News.query.filter_by(status='publicada').order_by(News.publication_date.desc()).all()
    sitemap_content = render_template('sitemap.xml', articles=articles, current_date=datetime.utcnow())
    response = make_response(sitemap_content)
    response.headers['Content-Type'] = 'application/xml'
    return response

# Admin routes
@app.route('/admin')
@login_required
def admin_dashboard():
    articles = News.query.order_by(News.publication_date.desc()).all()
    return render_template('admin/dashboard.html', articles=articles)

@app.route('/admin/news')
@login_required
def news_list():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('search', '')
    status_filter = request.args.get('status', '')
    category_filter = request.args.get('category', '')

    query = News.query.order_by(News.publication_date.desc())

    if search_query:
        query = query.filter(db.or_(
            News.title.ilike(f'%{search_query}%'),
            News.content.ilike(f'%{search_query}%')
        ))
    if status_filter:
        query = query.filter_by(status=status_filter)
    if category_filter:
        query = query.filter_by(category=category_filter)

    articles = query.paginate(page=page, per_page=10, error_out=False) # 10 artigos por página

    # Obter categorias únicas para o filtro
    unique_categories = [cat[0] for cat in db.session.query(News.category).distinct().all() if cat[0]]

    return render_template('admin/news_list.html', 
                           articles=articles, 
                           unique_categories=unique_categories,
                           search_query=search_query,
                           status_filter=status_filter,
                           category_filter=category_filter)

@app.route('/admin/news/new', methods=['GET', 'POST'])
@login_required
def new_news_article():
    if request.method == 'POST':
        print(f"DEBUG: Content-Length do cabeçalho: {request.headers.get('Content-Length')}")
        print(f"DEBUG: request.content_length: {request.content_length}")
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        category = request.form.get('category')
        tags = request.form.get('tags')
        meta_description = request.form.get('meta_description')
        status = request.form.get('status', 'rascunho')
        sources = request.form.get('sources')

        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while News.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1

        featured_image = None
        if 'image' in request.files and request.files['image'].filename != '':
            image_file = request.files['image']
            if image_file.content_length > app.config['MAX_CONTENT_LENGTH']:
                flash('Imagem muito grande! Tamanho máximo é 2MB.', 'danger')
                return redirect(request.url)
            if not allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                flash('Formato de imagem inválido. Apenas JPG, JPEG, PNG, WEBP são permitidos.', 'danger')
                return redirect(request.url)
            featured_image = save_and_resize_image(image_file)

        video_filename = None
        video_embed_url = request.form.get('video_embed_url')

        if 'video_file' in request.files and request.files['video_file'].filename != '':
            video_file = request.files['video_file']
            if video_file.content_length > 300 * 1024 * 1024:
                flash('Vídeo muito grande! Tamanho máximo é 300MB.', 'danger')
                return redirect(request.url)
            if not allowed_file(video_file.filename, ALLOWED_VIDEO_EXTENSIONS):
                flash('Formato de vídeo inválido. Apenas MP4, MOV, AVI, WEBM são permitidos.', 'danger')
                return redirect(request.url)
            filename = str(uuid.uuid4()) + '.' + video_file.filename.rsplit('.', 1)[1].lower()
            video_file.save(os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'], filename))
            video_filename = filename
            video_embed_url = None
        
        if video_embed_url and not ("youtube.com" in video_embed_url or "youtu.be" in video_embed_url or "vimeo.com" in video_embed_url):
            flash('URL de vídeo embedado inválida. Apenas YouTube ou Vimeo são permitidos.', 'danger')
            video_embed_url = None
        elif video_embed_url and video_filename:
             video_filename = None

        publication_date = datetime.utcnow()
        if request.form.get('publication_date'):
            try:
                publication_date = datetime.strptime(request.form['publication_date'], '%Y-%m-%dT%H:%M')
            except ValueError:
                flash('Formato de data inválido. Usando data e hora atuais.', 'warning')

        new_article = News(title=title, content=content, author=author,
                           publication_date=publication_date, category=category, tags=tags,
                           slug=slug, meta_description=meta_description, featured_image=featured_image,
                           status=status, sources=sources,
                           video_filename=video_filename, video_embed_url=video_embed_url)

        db.session.add(new_article)
        db.session.commit()
        flash('Notícia criada com sucesso!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/news_form.html')

@app.route('/admin/news/edit/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_news_article(article_id):
    article = News.query.get_or_404(article_id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.content = request.form['content']
        article.author = request.form['author']
        article.category = request.form.get('category')
        article.tags = request.form.get('tags')
        article.meta_description = request.form.get('meta_description')
        article.status = request.form.get('status', 'rascunho')
        article.sources = request.form.get('sources')
        
        new_slug = request.form.get('slug')
        if not new_slug or new_slug != article.slug:
            base_slug = slugify(article.title) if not new_slug else slugify(new_slug)
            slug = base_slug
            counter = 1
            while News.query.filter_by(slug=slug).filter(News.id != article.id).first():
                slug = f"{base_slug}-{counter}"
                counter += 1
            article.slug = slug

        if 'image' in request.files and request.files['image'].filename != '':
            image_file = request.files['image']
            if image_file.content_length > app.config['MAX_CONTENT_LENGTH']:
                flash('Imagem muito grande! Tamanho máximo é 2MB.', 'danger')
                return redirect(request.url)
            if not allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                flash('Formato de imagem inválido. Apenas JPG, JPEG, PNG, WEBP são permitidos.', 'danger')
                return redirect(request.url)
            
            if article.featured_image:
                for size in ['thumb', 'medium', 'original']:
                    old_path = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], size, article.featured_image)
                    if os.path.exists(old_path):
                        try: os.remove(old_path) 
                        except OSError: pass

            article.featured_image = save_and_resize_image(image_file)
        elif request.form.get('remove_image') == 'true':
            if article.featured_image:
                for size in ['thumb', 'medium', 'original']:
                    old_path = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], size, article.featured_image)
                    if os.path.exists(old_path):
                        try: os.remove(old_path)
                        except OSError: pass
                article.featured_image = None

        video_file_uploaded = False
        if 'video_file' in request.files and request.files['video_file'].filename != '':
            video_file = request.files['video_file']
            if video_file.content_length > 300 * 1024 * 1024:
                flash('Vídeo muito grande! Tamanho máximo é 300MB.', 'danger')
                return redirect(request.url)
            if not allowed_file(video_file.filename, ALLOWED_VIDEO_EXTENSIONS):
                flash('Formato de vídeo inválido. Apenas MP4, MOV, AVI, WEBM são permitidos.', 'danger')
                return redirect(request.url)

            if article.video_filename:
                try: os.remove(os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'], article.video_filename))
                except OSError: pass

            filename = str(uuid.uuid4()) + '.' + video_file.filename.rsplit('.', 1)[1].lower()
            video_file.save(os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'], filename))
            article.video_filename = filename
            article.video_embed_url = None
        elif request.form.get('remove_video_file') == 'true':
            if article.video_filename:
                try: os.remove(os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'], article.video_filename))
                except OSError: pass
                article.video_filename = None

        new_video_embed_url = request.form.get('video_embed_url')
        if new_video_embed_url and not ("youtube.com" in new_video_embed_url or "youtu.be" in new_video_embed_url or "vimeo.com" in new_video_embed_url):
            flash('URL de vídeo embedado inválida. Apenas YouTube ou Vimeo são permitidos.', 'danger')
            article.video_embed_url = None
        elif new_video_embed_url: 
            article.video_embed_url = new_video_embed_url
            article.video_filename = None 
        elif request.form.get('remove_video_embed_url') == 'true':
            article.video_embed_url = None

        if request.form.get('publication_date'):
            try:
                article.publication_date = datetime.strptime(request.form['publication_date'], '%Y-%m-%dT%H:%M')
            except ValueError:
                flash('Formato de data inválido. Mantendo data existente.', 'warning')

        db.session.commit()
        flash('Notícia atualizada com sucesso!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin/news_form.html', article=article)

@app.route('/admin/news/delete/<int:article_id>', methods=['POST'])
@login_required
def delete_news_article(article_id):
    article = News.query.get_or_404(article_id)
    # Delete associated files
    if article.featured_image:
        for size in ['thumb', 'medium', 'original']:
            old_path = os.path.join(app.config['UPLOAD_FOLDER_IMAGES'], size, article.featured_image)
            if os.path.exists(old_path):
                try: os.remove(old_path)
                except OSError: pass

    if article.video_filename:
        try: os.remove(os.path.join(app.config['UPLOAD_FOLDER_VIDEOS'], article.video_filename))
        except OSError: pass
    
    db.session.delete(article)
    db.session.commit()
    flash('Notícia excluída com sucesso!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login bem-sucedido!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Login inválido. Verifique o nome de usuário e a senha.', 'danger')
    return render_template('admin/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Você foi desconectado.', 'info')
    return redirect(url_for('index'))

@app.route('/admin/comments')
@login_required
def comments_list():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')

    query = Comment.query.order_by(Comment.publication_date.desc())

    if status_filter == 'approved':
        query = query.filter_by(approved=True)
    elif status_filter == 'pending':
        query = query.filter_by(approved=False)

    comments = query.paginate(page=page, per_page=10, error_out=False)
    return render_template('admin/comments_list.html', comments=comments, status_filter=status_filter)

@app.route('/admin/comment/approve/<int:comment_id>', methods=['POST'])
@login_required
def approve_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.approved = True
    db.session.commit()
    flash('Comentário aprovado com sucesso!', 'success')
    return redirect(url_for('comments_list'))

@app.route('/admin/comment/delete/<int:comment_id>', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comentário excluído com sucesso!', 'success')
    return redirect(url_for('comments_list'))

if __name__ == '__main__':
    # Initialize the database and create a default admin user if it doesn't exist
    with app.app_context():
        db.create_all()
        # Create a default admin user if one doesn't exist
        if not User.query.filter_by(username='admin').first():
            admin_user = User(username='admin', role='admin')
            admin_user.set_password('admin_password') # IMPORTANT: Change this in production!
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user 'admin' created with password 'admin_password'. PLEASE CHANGE THIS IN PRODUCTION!")

    app.run(debug=True) 