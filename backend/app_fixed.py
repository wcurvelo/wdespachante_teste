from flask import request, redirect, url_for, flash, render_template
from slugify import slugify
from datetime import datetime
import os

def create_edit_news(id=None):
    """
    Cria ou edita uma notícia
    """
    from app import db, News, app
    
    if id:
        article = News.query.get_or_404(id)
        if request.method == 'POST':
            # Lógica para edição de notícia existente
            pass
        return render_template('admin/news_form.html', article=article)
    
    # Criação de nova notícia
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        category = request.form.get('category')
        tags = request.form.get('tags')
        meta_description = request.form.get('meta_description')
        status = request.form.get('status', 'draft')
        sources = request.form.get('sources')
        is_featured = 'is_featured' in request.form
        allow_comments = 'allow_comments' in request.form
        social_title = request.form.get('social_title')
        social_description = request.form.get('social_description')
        
        # Slug manual ou gerado automaticamente
        if request.form.get('slug'):
            slug = slugify(request.form.get('slug'))
        else:
            slug = slugify(title)
            
        # Verificar se o slug já existe
        base_slug = slug
        counter = 1
        while News.query.filter_by(slug=slug).first():
            slug = f"{base_slug}-{counter}"
            counter += 1
        
        # Processar imagem destacada
        featured_image = None
        if 'featured_image' in request.files and request.files['featured_image'].filename != '':
            image_file = request.files['featured_image']
            if not allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                flash('Formato de imagem inválido. Apenas JPG, JPEG, PNG, WEBP são permitidos.', 'error')
                return redirect(request.url)
            
            featured_image = save_and_resize_image(image_file)
        
        # Processar galeria de imagens
        gallery_images = []
        if 'gallery_images' in request.files:
            gallery_files = request.files.getlist('gallery_images')
            for image_file in gallery_files:
                if image_file.filename != '':
                    if not allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                        continue
                    image_filename = save_and_resize_image(image_file)
                    if image_filename:
                        gallery_images.append(image_filename)
        
        gallery_images_str = ','.join(gallery_images) if gallery_images else None
        
        # Processar URL do vídeo
        video_url = request.form.get('video_url')
        video_embed_url = None
        if video_url:
            video_embed_url = get_embed_url(video_url)
        
        # Processar upload de vídeo
        video_filename = None
        if 'video_file' in request.files and request.files['video_file'].filename != '':
            video_file = request.files['video_file']
            if not allowed_file(video_file.filename, ALLOWED_VIDEO_EXTENSIONS):
                flash('Formato de vídeo inválido. Apenas MP4, MOV, AVI, WEBM são permitidos.', 'error')
                return redirect(request.url)
            
            # Processar o vídeo para padronização
            video_filename = process_video(video_file)
            
            # Se temos um vídeo de upload, ignoramos a URL de vídeo
            if video_filename and video_embed_url:
                video_embed_url = None

        publish_date = None
        if status == 'scheduled' and request.form.get('publish_date'):
            try:
                publish_date = datetime.strptime(request.form['publish_date'], '%Y-%m-%dT%H:%M')
            except ValueError:
                flash('Formato de data inválido. Usando data e hora atuais.', 'warning')
                publish_date = datetime.now()
        else:
            publish_date = datetime.now()

        try:
            new_article = News(
                title=title, 
                content=content, 
                author=author,
                publication_date=publish_date, 
                category=category, 
                tags=tags,
                slug=slug, 
                meta_description=meta_description, 
                featured_image=featured_image,
                status=status, 
                sources=sources,
                video_filename=video_filename, 
                video_embed_url=video_embed_url,
                video_url=video_url,
                gallery_images=gallery_images_str,
                is_featured=is_featured,
                allow_comments=allow_comments,
                social_title=social_title,
                social_description=social_description
            )
            
            db.session.add(new_article)
            db.session.commit()
            flash('Notícia criada com sucesso!', 'success')
            return redirect(url_for('news_list'))
        except Exception as e:
            db.session.rollback()
            flash(f'Erro ao criar notícia: {str(e)}', 'error')
            print(f"ERRO: {str(e)}")
            return redirect(request.url)
    
    return render_template('admin/news_form.html') 