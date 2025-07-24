// Inicializar a galeria de imagens
function initGallery(galleryImagesArray) {
    var galleryItems = document.querySelectorAll('.gallery-item');
    var lightbox = document.querySelector('.lightbox');
    var lightboxContent = document.querySelector('.lightbox-content');
    var lightboxClose = document.querySelector('.lightbox-close');
    var lightboxPrev = document.querySelector('.lightbox-prev');
    var lightboxNext = document.querySelector('.lightbox-next');
    
    var currentIndex = 0;
    var galleryImages = galleryImagesArray;
    
    // Abrir lightbox ao clicar em uma imagem da galeria
    for (var i = 0; i < galleryItems.length; i++) {
        (function(index) {
            galleryItems[index].addEventListener('click', function() {
                currentIndex = parseInt(this.getAttribute('data-index'));
                showImage(currentIndex);
                lightbox.classList.add('active');
            });
        })(i);
    }
    
    // Fechar lightbox
    lightboxClose.addEventListener('click', function() {
        lightbox.classList.remove('active');
    });
    
    // Navegar para a imagem anterior
    lightboxPrev.addEventListener('click', function() {
        currentIndex = (currentIndex - 1 + galleryImages.length) % galleryImages.length;
        showImage(currentIndex);
    });
    
    // Navegar para a próxima imagem
    lightboxNext.addEventListener('click', function() {
        currentIndex = (currentIndex + 1) % galleryImages.length;
        showImage(currentIndex);
    });
    
    // Fechar lightbox ao clicar fora da imagem
    lightbox.addEventListener('click', function(e) {
        if (e.target === lightbox) {
            lightbox.classList.remove('active');
        }
    });
    
    // Mostrar a imagem atual
    function showImage(index) {
        lightboxContent.src = galleryImages[index];
    }
    
    // Navegação pelo teclado
    document.addEventListener('keydown', function(e) {
        if (!lightbox.classList.contains('active')) return;
        
        if (e.key === 'Escape') {
            lightbox.classList.remove('active');
        } else if (e.key === 'ArrowLeft') {
            currentIndex = (currentIndex - 1 + galleryImages.length) % galleryImages.length;
            showImage(currentIndex);
        } else if (e.key === 'ArrowRight') {
            currentIndex = (currentIndex + 1) % galleryImages.length;
            showImage(currentIndex);
        }
    });
} 