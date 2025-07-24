from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from slugify import slugify
import bcrypt

db = SQLAlchemy()

# Tabela de associação entre notícias e tags
news_tags = db.Table('news_tags',
    db.Column('news_id', db.Integer, db.ForeignKey('news.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(80), default='redator') # admin, editor, redator, revisor
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    news_articles = db.relationship('News', backref='author_user', lazy=True, foreign_keys='News.author_id')

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f'<User {self.username}>'

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    slug = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relacionamentos
    news_articles = db.relationship('News', backref='category_rel', lazy=True)
    subcategories = db.relationship('Category', backref=db.backref('parent', remote_side=[id]), lazy=True)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.slug and self.name:
            self.slug = self.generate_slug(self.name)
    
    def generate_slug(self, name):
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        while Category.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    slug = db.Column(db.String(50), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    # Relacionamentos através da tabela de associação news_tags
    news_articles = db.relationship('News', secondary=news_tags, lazy='subquery', backref=db.backref('tags_rel', lazy=True))
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.slug and self.name:
            self.slug = self.generate_slug(self.name)
    
    def generate_slug(self, name):
        base_slug = slugify(name)
        slug = base_slug
        counter = 1
        while Tag.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug
    
    def __repr__(self):
        return f'<Tag {self.name}>'

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False) # Nome do autor (para compatibilidade)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Relacionamento com o usuário autor
    publication_date = db.Column(db.DateTime, default=datetime.now)
    publish_date = db.Column(db.DateTime, default=datetime.now)  # Alias para compatibilidade
    category = db.Column(db.String(100), nullable=True) # Categoria como string (para compatibilidade)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True) # Relacionamento com a categoria
    tags = db.Column(db.String(255), nullable=True) # Tags como string (para compatibilidade)
    slug = db.Column(db.String(255), unique=True, nullable=False)
    meta_description = db.Column(db.String(160), nullable=True)
    summary = db.Column(db.Text, nullable=True)  # Resumo do artigo
    featured_image = db.Column(db.String(255), nullable=True) # URL ou caminho do arquivo
    gallery_images = db.Column(db.Text, nullable=True) # Lista de imagens separadas por vírgula
    video_filename = db.Column(db.String(255), nullable=True) # Caminho para vídeo de upload direto
    video_embed_url = db.Column(db.String(255), nullable=True) # URL para vídeo embedado (YouTube, Vimeo)
    video_url = db.Column(db.String(255), nullable=True) # URL para vídeo (YouTube, Vimeo)
    video = db.Column(db.String(255), nullable=True)  # Alias para compatibilidade
    video_embed = db.Column(db.String(255), nullable=True)  # Alias para compatibilidade
    status = db.Column(db.String(50), default='draft') # draft, published, scheduled
    sources = db.Column(db.Text, nullable=True) # Armazenar como JSON string ou texto
    is_featured = db.Column(db.Boolean, default=False) # Destaque na página inicial
    allow_comments = db.Column(db.Boolean, default=True) # Permitir comentários
    social_title = db.Column(db.String(200), nullable=True) # Título para redes sociais
    social_description = db.Column(db.Text, nullable=True) # Descrição para redes sociais
    comments = db.relationship('Comment', backref='news_article', lazy=True, 
                              foreign_keys='Comment.news_article_id', cascade="all, delete-orphan")
    images = db.relationship('NewsImage', backref='news', lazy=True, cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.slug and self.title:
            self.slug = self.generate_slug(self.title)

    def generate_slug(self, title):
        base_slug = slugify(title)
        slug = base_slug
        counter = 1
        while News.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        return slug
        
    @property
    def publish_date(self):
        return self.publication_date
        
    @property
    def video(self):
        return self.video_filename
        
    @property
    def video_embed(self):
        return self.video_embed_url

    def __repr__(self):
        return f'<News {self.title}>'

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    news_article_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True) # Opcional: para notificações ou contato
    content = db.Column(db.Text, nullable=False)
    publication_date = db.Column(db.DateTime, default=datetime.now)
    created_at = db.Column(db.DateTime, default=datetime.now)  # Alias para compatibilidade
    approved = db.Column(db.Boolean, default=False) # Para moderação

    def __init__(self, *args, **kwargs):
        if 'name' in kwargs and not 'author' in kwargs:
            kwargs['author'] = kwargs['name']
        if 'news_id' in kwargs and not 'news_article_id' in kwargs:
            kwargs['news_article_id'] = kwargs['news_id']
        super().__init__(*args, **kwargs)
        
    @property
    def name(self):
        return self.author
        
    @property
    def created_at(self):
        return self.publication_date

    def __repr__(self):
        return f'<Comment {self.author} - Article {self.news_article_id}>'
        
class NewsImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'), nullable=False)
    image_filename = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(255))
    order = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<NewsImage {self.image_filename}>'

class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False)
    icon = db.Column(db.String(100), nullable=True)
    summary = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=True)
    active = db.Column(db.Boolean, default=True)
    featured = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)

    def __init__(self, *args, **kwargs):
        if 'name' in kwargs and not self.slug:
            self.slug = slugify(kwargs['name'])
        super(Service, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f'<Service "{self.name}">'

class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=True)  # Cidade/Estado
    content = db.Column(db.Text, nullable=False)  # Texto do depoimento
    image = db.Column(db.String(255), nullable=True)  # Foto da pessoa
    rating = db.Column(db.Integer, default=5)  # Avaliação de 1 a 5
    featured = db.Column(db.Boolean, default=False)  # Destaque na página inicial
    order = db.Column(db.Integer, default=0)  # Ordem de exibição
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<Testimonial {self.name}>'

class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(255), nullable=False)
    answer = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(100), nullable=True)  # Categoria da pergunta
    order = db.Column(db.Integer, default=0)  # Ordem de exibição
    featured = db.Column(db.Boolean, default=False)  # Destaque na página inicial
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<FAQ {self.question[:30]}...>'

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    service = db.Column(db.String(100), nullable=True)  # Serviço de interesse
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='new')  # new, read, replied, archived
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f'<ContactMessage {self.name} - {self.created_at}>'

class Detran(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(50), nullable=False)  # Nome do estado
    state_abbr = db.Column(db.String(2), nullable=False)  # Sigla do estado (UF)
    name = db.Column(db.String(100), nullable=False)  # Nome do Detran
    url = db.Column(db.String(255), nullable=False)  # URL do site oficial
    region = db.Column(db.String(20), nullable=False)  # Região do Brasil (Norte, Nordeste, etc.)
    description = db.Column(db.Text, nullable=True)  # Descrição ou informações adicionais
    flag_image = db.Column(db.String(255), nullable=True)  # Imagem da bandeira do estado
    order = db.Column(db.Integer, default=0)  # Ordem de exibição
    
    def __repr__(self):
        return f'<Detran {self.state_abbr} - {self.state}>'

class LinkUtil(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(50), nullable=True)  # Categoria do link (Detran, Governo, etc.)
    icon = db.Column(db.String(50), nullable=True)  # Nome do ícone
    order = db.Column(db.Integer, default=0)  # Ordem de exibição
    featured = db.Column(db.Boolean, default=False)  # Destaque na página inicial
    created_at = db.Column(db.DateTime, default=datetime.now)
    
    def __repr__(self):
        return f'<LinkUtil {self.title}>' 