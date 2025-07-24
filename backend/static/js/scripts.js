document.addEventListener('DOMContentLoaded', function() {
    const backToTopButton = document.getElementById('back-to-top');
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTopButton.classList.remove('hidden');
            setTimeout(() => {
                backToTopButton.style.opacity = '1';
                backToTopButton.style.transform = 'scale(1) translateY(0)';
            }, 50);
        } else {
            backToTopButton.style.opacity = '0';
            backToTopButton.style.transform = 'scale(0.95) translateY(1rem)';
            setTimeout(() => {
                backToTopButton.classList.add('hidden');
            }, 300);
        }
    });
    
    backToTopButton.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
        // Add click feedback animation
        this.style.transform = 'scale(0.95)';
        setTimeout(() => {
            this.style.transform = 'scale(1)';
        }, 200);
    });
    
    backToTopButton.addEventListener('mouseover', () => {
        if (window.pageYOffset > 300) {
            backToTopButton.style.transform = 'scale(1.1) translateY(0)';
        }
    });
    
    backToTopButton.addEventListener('mouseout', () => {
        if (window.pageYOffset > 300) {
            backToTopButton.style.transform = 'scale(1) translateY(0)';
        }
    });
    
    // Função para animar contadores
    function animateValue(element, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            element.textContent = Math.floor(progress * (end - start) + start).toLocaleString();
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }
    
    // Inicializar contador de visitantes
    function initVisitorCounter() {
        const visitorCount = document.getElementById('visitor-count');
        const onlineCount = document.getElementById('online-count');
        const todayCount = document.getElementById('today-count');
        
        if (visitorCount && onlineCount && todayCount) {
            const totalVisitors = 15783;
            const onlineVisitors = Math.floor(Math.random() * (50 - 30 + 1)) + 30;
            const todayVisitors = Math.floor(Math.random() * (500 - 300 + 1)) + 300;
            
            animateValue(visitorCount, 0, totalVisitors, 2000);
            animateValue(onlineCount, 0, onlineVisitors, 1500);
            animateValue(todayCount, 0, todayVisitors, 1500);
            
            setInterval(() => {
                const newOnlineCount = Math.floor(Math.random() * (50 - 30 + 1)) + 30;
                animateValue(onlineCount, parseInt(onlineCount.textContent.replace(/,/g, '')), newOnlineCount, 1000);
            }, 10000);
        }
    }
    
    // Adicionar estilos de animação para o botão de WhatsApp
    const style = document.createElement('style');
    style.textContent = `
        @keyframes ping {
            0% {
                transform: scale(1);
                opacity: 1;
            }
            75%, 100% {
                transform: scale(2);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
    
    // Inicializar contador de visitantes
    initVisitorCounter();
    
    // Menu mobile
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (mobileMenuButton && mobileMenu) {
        mobileMenuButton.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
    
    // Navegação com smooth scroll
    const navLinks = document.querySelectorAll('a[href^="#"]');
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            if (mobileMenu && !mobileMenu.classList.contains('hidden')) {
                mobileMenu.classList.add('hidden');
            }
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Carregar depoimentos de clientes
    function fetchGoogleReviews() {
        const slider = document.getElementById('testimonials-slider');
        if (!slider) return;
        
        slider.innerHTML = '';
        const reviews = [
            {
                text: "Serviço excelente, bom preço e equipe super atenciosa!!!",
                name: "Douglas Ianov",
                rating: 5,
                time: "um mês atrás"
            },
            {
                text: "Super indico Wellington despachante!!!! Atendimento, comprometimento, dedicação e competência!!!! Nota 1000 👏 👏 👏",
                name: "Fabio Leonardo",
                rating: 5,
                time: "3 meses atrás"
            },
            {
                text: "Ótimo atendimento, boa educação e atenção.",
                name: "Milena Baio",
                rating: 5,
                time: "4 meses atrás"
            },
            {
                text: "Depois de uma péssima experiência com um despachante me indicaram a Wellington Despachante RJ. Foi uma excelente experiência, não só resolveram meu problema em tempo como me deu esperança que ainda tem gente boa e profissionais competentes nesse mundo. Muito obrigado Wellington despachante Rj!",
                name: "Anderson Brito Meira",
                rating: 5,
                time: "3 anos atrás"
            },
            {
                text: "Excelente profissional! Wellington despachante conseguiu resolver com bastante profissionalismo o meu processo. Muito educado e atencioso.",
                name: "Tassia Garcia",
                rating: 5,
                time: "2 anos atrás"
            },
            {
                text: "Excelente profissional, resolvendo as questões com notável eficiência e confiabilidade. Fui muito bem atendido.",
                name: "Claudio Siqueira Vianna",
                rating: 5,
                time: "6 anos atrás"
            },
            {
                text: "Experiência excelente! Atendimento rápido e eficiente! Preço justo! Recomendo muito!",
                name: "Aurélien Maudonnet",
                rating: 5,
                time: "3 anos atrás"
            },
            {
                text: "De extrema confiança e sempre resolveu todas as pendências e problemas que surgiram em meus carros.",
                name: "Luiz Marcelo Badan",
                rating: 5,
                time: "2 anos atrás"
            },
            {
                text: "Profissional sério e comprometido. Transmite tranquilidade e segurança na execução dos serviços. Recomendo.",
                name: "Marcelo Couto (Escuderia Cataldi)",
                rating: 5,
                time: "6 anos atrás"
            },
            {
                text: "Excelente condução e profissionalismo. Recomendo muito 👏 👏 👏 👏",
                name: "Athos de Sá",
                rating: 5,
                time: "um ano atrás"
            },
            {
                text: "Serviço sem falhas e com prazos cumpridos recomendo!",
                name: "Bens Perpetuum Consultoria",
                rating: 5,
                time: "3 anos atrás"
            },
            {
                text: "Excelente serviço prestado. Recomendo.",
                name: "Isaac Azevedo",
                rating: 5,
                time: "3 anos atrás"
            },
            {
                text: "Ótimo, muito bom",
                name: "Paulo Cesar Barbosa Travassos",
                rating: 5,
                time: "3 anos atrás"
            },
            {
                text: "Wellington é um excelente despachante, ótimo atendimento e eficiência nos processos.",
                name: "Sandro Renjer",
                rating: 5,
                time: "7 anos atrás"
            },
            {
                text: "Recomendo Wellington 100%",
                name: "Leabdro Carvalho",
                rating: 5,
                time: "2 anos atrás"
            }
        ];
        
        reviews.forEach(review => {
            const reviewElement = document.createElement('div');
            reviewElement.className = 'w-full lg:w-1/3 flex-shrink-0 px-4';
            reviewElement.innerHTML = `
                <div class="bg-white p-6 rounded shadow-sm h-full">
                    <div class="flex items-center text-yellow-400 mb-4">
                        ${'<i class="ri-star-fill"></i>'.repeat(5)}
                    </div>
                    <p class="text-gray-600 mb-4">"${review.text}"</p>
                    <div class="flex items-center">
                        <div class="w-12 h-12 bg-gray-200 rounded-full flex items-center justify-center text-gray-500">
                            <i class="ri-user-line"></i>
                        </div>
                        <div class="ml-3">
                            <p class="font-medium">${review.name}</p>
                            <p class="text-sm text-gray-500">★ ${review.rating}.0 · ${review.time}</p>
                        </div>
                    </div>
                </div>
            `;
            slider.appendChild(reviewElement);
        });
        
        initializeTestimonialSlider();
    }
    
    // Inicializar slider de depoimentos
    function initializeTestimonialSlider() {
        const slider = document.getElementById('testimonials-slider');
        const prevButton = document.getElementById('prev-testimonial');
        const nextButton = document.getElementById('next-testimonial');
        const dotsContainer = document.getElementById('testimonial-dots');
        const testimonialContainer = document.getElementById('testimonials-container');
        
        if (!slider || !prevButton || !nextButton || !dotsContainer) return;
        
        const testimonials = slider.children;
        const totalTestimonials = testimonials.length;
        let currentIndex = 0;
        let autoplayInterval;
        
        function createDots() {
            dotsContainer.innerHTML = '';
            const slidesPerView = window.innerWidth >= 1024 ? 3 : 1;
            const totalDots = Math.ceil(totalTestimonials / slidesPerView);
            
            for (let i = 0; i < totalDots; i++) {
                const dot = document.createElement('button');
                dot.classList.add('w-8', 'h-2', 'rounded-full', 'bg-gray-300', 'hover:bg-gray-400', 'transition-all', 'duration-300', 'mx-1');
                dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
                dot.addEventListener('click', () => goToSlide(i * slidesPerView));
                dotsContainer.appendChild(dot);
            }
            updateDots();
        }
        
        function updateDots() {
            const dots = dotsContainer.children;
            const slidesPerView = window.innerWidth >= 1024 ? 3 : 1;
            
            for (let i = 0; i < dots.length; i++) {
                const isActive = i === Math.floor(currentIndex / slidesPerView);
                dots[i].classList.remove('bg-primary', 'w-12', 'bg-gray-300');
                dots[i].classList.add(isActive ? 'bg-primary' : 'bg-gray-300');
                dots[i].style.width = isActive ? '32px' : '24px';
            }
        }
        
        function updateSliderPosition() {
            if (testimonials.length === 0) return;
            
            const slideWidth = testimonials[0].offsetWidth;
            const slidesPerView = window.innerWidth >= 1024 ? 3 : 1;
            const maxTranslate = (totalTestimonials - slidesPerView) * slideWidth;
            const translate = Math.min(currentIndex * slideWidth, maxTranslate);
            
            slider.style.transform = `translateX(-${translate}px)`;
            slider.style.transition = 'transform 0.5s ease-in-out';
            updateDots();
            checkSliderButtons();
        }
        
        function checkSliderButtons() {
            if (currentIndex === 0) {
                prevButton.classList.add('opacity-50', 'cursor-not-allowed');
                prevButton.disabled = true;
            } else {
                prevButton.classList.remove('opacity-50', 'cursor-not-allowed');
                prevButton.disabled = false;
            }
            
            const slidesPerView = window.innerWidth >= 1024 ? 3 : 1;
            if (currentIndex >= totalTestimonials - slidesPerView) {
                nextButton.classList.add('opacity-50', 'cursor-not-allowed');
                nextButton.disabled = true;
            } else {
                nextButton.classList.remove('opacity-50', 'cursor-not-allowed');
                nextButton.disabled = false;
            }
        }
        
        function goToSlide(index) {
            currentIndex = index;
            updateSliderPosition();
        }
        
        function nextSlide() {
            const slidesPerView = window.innerWidth >= 1024 ? 3 : 1;
            if (currentIndex < totalTestimonials - slidesPerView) {
                currentIndex += 1;
                updateSliderPosition();
            } else {
                // Loop back to first slide for autoplay
                currentIndex = 0;
                updateSliderPosition();
            }
        }
        
        function prevSlide() {
            if (currentIndex > 0) {
                currentIndex -= 1;
                updateSliderPosition();
            }
        }
        
        // Start autoplay - alternando a cada 6 segundos
        function startAutoplay() {
            stopAutoplay();
            autoplayInterval = setInterval(nextSlide, 6000);
        }
        
        function stopAutoplay() {
            if (autoplayInterval) {
                clearInterval(autoplayInterval);
            }
        }
        
        // Adicionar eventos
        nextButton.addEventListener('click', () => {
            stopAutoplay();
            nextSlide();
            startAutoplay();
        });
        
        prevButton.addEventListener('click', () => {
            stopAutoplay();
            prevSlide();
            startAutoplay();
        });
        
        // Parar autoplay quando o usuário interage com o slider
        testimonialContainer.addEventListener('mouseenter', () => {
            stopAutoplay();
        });
        
        testimonialContainer.addEventListener('mouseleave', () => {
            startAutoplay();
        });
        
        window.addEventListener('resize', updateSliderPosition);
        
        // Inicializar
        createDots();
        updateSliderPosition();
        startAutoplay(); // Inicia o autoplay
    }
    
    // Carregar os depoimentos
    fetchGoogleReviews();
    
    // Validação e envio do formulário de contato
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Verificar se todos os campos obrigatórios estão preenchidos
            const nome = document.getElementById('nome').value.trim();
            const email = document.getElementById('email').value.trim();
            const telefone = document.getElementById('telefone').value.trim();
            const servico = document.getElementById('servico').value;
            const mensagem = document.getElementById('mensagem').value.trim();
            
            let isValid = true;
            let errorMessage = '';
            
            if (!nome) {
                isValid = false;
                errorMessage = 'Por favor, preencha seu nome completo.';
            } else if (!email) {
                isValid = false;
                errorMessage = 'Por favor, preencha seu e-mail.';
            } else if (!validateEmail(email)) {
                isValid = false;
                errorMessage = 'Por favor, insira um e-mail válido.';
            } else if (!telefone) {
                isValid = false;
                errorMessage = 'Por favor, preencha seu telefone.';
            } else if (!servico) {
                isValid = false;
                errorMessage = 'Por favor, selecione um serviço de interesse.';
            } else if (!mensagem) {
                isValid = false;
                errorMessage = 'Por favor, escreva uma mensagem.';
            }
            
            if (!isValid) {
                alert(errorMessage);
                return;
            }
            
            // Se chegou aqui, o formulário é válido
            // Mostramos uma mensagem de carregamento
            const submitButton = document.getElementById('send-button');
            const formMessage = document.getElementById('form-message');
            submitButton.innerHTML = '<span class="animate-pulse">Enviando...</span>';
            submitButton.disabled = true;
            
            // Criar URL para envio via WhatsApp como alternativa
            const whatsappText = `*Nova mensagem do site*%0A%0A*Nome:* ${nome}%0A*Email:* ${email}%0A*Telefone:* ${telefone}%0A*Serviço:* ${servico}%0A%0A*Mensagem:*%0A${mensagem}`;
            const whatsappUrl = `https://wa.me/5521964474147?text=${encodeURIComponent(whatsappText)}`;
            
            // Mostrar mensagem de sucesso alternativa com link para WhatsApp
            formMessage.innerHTML = `
                <div class="bg-green-100 text-green-700 p-4 rounded">
                    <p class="font-medium mb-2">Formulário processado!</p>
                    <p class="mb-4">Para garantir uma resposta mais rápida, clique no botão abaixo e envie sua mensagem diretamente pelo WhatsApp.</p>
                    <a href="${whatsappUrl}" target="_blank" class="inline-block bg-green-500 text-white px-4 py-2 rounded font-medium hover:bg-green-600 transition-colors">
                        <i class="ri-whatsapp-line mr-1"></i> Enviar via WhatsApp
                    </a>
                </div>
            `;
            formMessage.classList.remove('hidden');
            
            // Limpar o formulário
            contactForm.reset();
            
            // Restaurar o botão após 3 segundos
            setTimeout(() => {
                submitButton.innerHTML = 'Enviar Mensagem';
                submitButton.disabled = false;
            }, 3000);
        });
    }
    
    // Função para validar e-mail
    function validateEmail(email) {
        const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(email);
    }
});

// Função para expandir/contrair as perguntas frequentes
function toggleFaq(element) {
    const content = element.nextElementSibling;
    const icon = element.querySelector('.faq-icon');
    
    if (content.classList.contains('hidden')) {
        content.classList.remove('hidden');
        icon.classList.remove('ri-arrow-down-s-line');
        icon.classList.add('ri-arrow-up-s-line');
        element.setAttribute('aria-expanded', 'true');
    } else {
        content.classList.add('hidden');
        icon.classList.remove('ri-arrow-up-s-line');
        icon.classList.add('ri-arrow-down-s-line');
        element.setAttribute('aria-expanded', 'false');
    }
} 

// Função para inicializar o editor TinyMCE
function initTinyMCE() {
    if (typeof tinymce !== 'undefined') {
        tinymce.init({
            selector: '#content',
            language: 'pt_BR',
            plugins: 'anchor autolink charmap codesample emoticons image link lists media searchreplace table visualblocks wordcount',
            toolbar: 'undo redo | blocks fontfamily fontsize | bold italic underline strikethrough | link image media table | align lineheight | numlist bullist indent outdent | emoticons charmap | removeformat',
            height: 500,
            images_upload_url: '/admin/upload-image',
            images_upload_handler: function (blobInfo, progress) {
                return new Promise((resolve, reject) => {
                    const xhr = new XMLHttpRequest();
                    xhr.withCredentials = false;
                    xhr.open('POST', '/admin/upload-image');
                    
                    xhr.upload.onprogress = (e) => {
                        progress(e.loaded / e.total * 100);
                    };
                    
                    xhr.onload = function() {
                        if (xhr.status === 403) {
                            reject({ message: 'HTTP Error: ' + xhr.status, remove: true });
                            return;
                        }
                        
                        if (xhr.status < 200 || xhr.status >= 300) {
                            reject('HTTP Error: ' + xhr.status);
                            return;
                        }
                        
                        const json = JSON.parse(xhr.responseText);
                        
                        if (!json || typeof json.location != 'string') {
                            reject('Invalid JSON: ' + xhr.responseText);
                            return;
                        }
                        
                        resolve(json.location);
                    };
                    
                    xhr.onerror = function () {
                        reject('Image upload failed due to a XHR Transport error');
                    };
                    
                    const formData = new FormData();
                    formData.append('file', blobInfo.blob(), blobInfo.filename());
                    
                    xhr.send(formData);
                });
            }
        });
    }
}

// Função para auto-gerar slug a partir do título
function initSlugGenerator() {
    const titleInput = document.getElementById('title');
    const slugInput = document.getElementById('slug');
    
    if (titleInput && slugInput) {
        titleInput.addEventListener('input', function() {
            const title = this.value;
            const slug = title
                .toLowerCase()
                .normalize('NFD')
                .replace(/[\u0300-\u036f]/g, '')
                .replace(/[^a-z0-9]+/g, '-')
                .replace(/(^-|-$)/g, '');
            slugInput.value = slug;
        });
    }
}

// Função para validar tamanho do resumo
function initSummaryValidator() {
    const summaryInput = document.getElementById('summary');
    
    if (summaryInput) {
        summaryInput.addEventListener('input', function() {
            if (this.value.length > 200) {
                this.value = this.value.substring(0, 200);
            }
        });
    }
}

// Função para preview de imagem
function initImagePreview() {
    const imageInput = document.getElementById('image');
    const previewContainer = document.createElement('div');
    previewContainer.className = 'image-preview';
    
    if (imageInput) {
        imageInput.parentNode.insertBefore(previewContainer, imageInput.nextSibling);
        
        imageInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                
                reader.onload = function(e) {
                    previewContainer.innerHTML = `
                        <img src="${e.target.result}" alt="Preview" style="max-width: 200px; margin-top: 1rem;">
                    `;
                };
                
                reader.readAsDataURL(file);
            } else {
                previewContainer.innerHTML = '';
            }
        });
    }
}

// Função para confirmação de exclusão
function initDeleteConfirmation() {
    const deleteButtons = document.querySelectorAll('.btn-delete');
    
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Tem certeza que deseja excluir este item?')) {
                e.preventDefault();
            }
        });
    });
}

// Mobile menu toggle
const menuToggle = document.querySelector('.menu-toggle');
const mainNav = document.querySelector('.main-nav ul');

if (menuToggle && mainNav) {
    menuToggle.addEventListener('click', function() {
        mainNav.classList.toggle('active');
        menuToggle.classList.toggle('active');
    });
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const targetId = this.getAttribute('href');
        if (targetId === '#') return;
        
        const targetElement = document.querySelector(targetId);
        if (targetElement) {
            window.scrollTo({
                top: targetElement.offsetTop - 80,
                behavior: 'smooth'
            });
            
            // Update URL
            history.pushState(null, null, targetId);
        }
    });
});

// Back to top button
const backToTopBtn = document.createElement('button');
backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
backToTopBtn.className = 'back-to-top';
backToTopBtn.style.display = 'none';
document.body.appendChild(backToTopBtn);

backToTopBtn.addEventListener('click', function() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

window.addEventListener('scroll', function() {
    if (window.pageYOffset > 300) {
        backToTopBtn.style.display = 'block';
    } else {
        backToTopBtn.style.display = 'none';
    }
});

// Add styles for back to top button
const style = document.createElement('style');
style.innerHTML = `
    .back-to-top {
        position: fixed;
        bottom: 20px;
        right: 20px;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: var(--primary-color);
        color: white;
        border: none;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.2rem;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        transition: all 0.3s;
        z-index: 1000;
    }
    
    .back-to-top:hover {
        background-color: var(--secondary-color);
        transform: translateY(-3px);
    }
`;
document.head.appendChild(style);

// Mobile menu toggle styles and HTML
if (document.querySelector('.site-header') && !document.querySelector('.menu-toggle')) {
    const menuToggleBtn = document.createElement('button');
    menuToggleBtn.className = 'menu-toggle';
    menuToggleBtn.innerHTML = '<span></span><span></span><span></span>';
    document.querySelector('.site-header').appendChild(menuToggleBtn);
    
    const menuStyle = document.createElement('style');
    menuStyle.innerHTML = `
        .menu-toggle {
            display: none;
            background: transparent;
            border: none;
            cursor: pointer;
            padding: 0;
            width: 30px;
            height: 20px;
            position: relative;
            z-index: 1001;
        }
        
        .menu-toggle span {
            display: block;
            width: 100%;
            height: 2px;
            background-color: white;
            margin-bottom: 5px;
            transition: all 0.3s;
        }
        
        .menu-toggle span:last-child {
            margin-bottom: 0;
        }
        
        .menu-toggle.active span:nth-child(1) {
            transform: translateY(7px) rotate(45deg);
        }
        
        .menu-toggle.active span:nth-child(2) {
            opacity: 0;
        }
        
        .menu-toggle.active span:nth-child(3) {
            transform: translateY(-7px) rotate(-45deg);
        }
        
        @media (max-width: 768px) {
            .menu-toggle {
                display: block;
            }
            
            .main-nav ul {
                display: none;
                position: absolute;
                top: 60px;
                left: 0;
                width: 100%;
                background-color: var(--dark-bg);
                flex-direction: column;
                padding: 1rem 0;
                box-shadow: 0 5px 10px rgba(0, 0, 0, 0.1);
                z-index: 1000;
            }
            
            .main-nav ul.active {
                display: flex;
            }
            
            .main-nav li {
                margin: 0;
                width: 100%;
                text-align: center;
            }
            
            .main-nav a {
                display: block;
                padding: 0.75rem 0;
            }
            
            .site-header {
                position: relative;
            }
        }
    `;
    document.head.appendChild(menuStyle);
}

// Lightbox gallery
const galleryItems = document.querySelectorAll('.gallery-item');
if (galleryItems.length > 0) {
    const lightbox = document.querySelector('.lightbox') || createLightbox();
    
    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const img = this.querySelector('img');
            const src = img.src.replace('/thumb/', '/medium/');
            const lightboxImg = lightbox.querySelector('.lightbox-content');
            lightboxImg.src = src;
            lightbox.classList.add('active');
        });
    });
    
    function createLightbox() {
        const lightbox = document.createElement('div');
        lightbox.className = 'lightbox';
        lightbox.innerHTML = `
            <span class="lightbox-close">&times;</span>
            <img class="lightbox-content">
        `;
        document.body.appendChild(lightbox);
        
        const closeBtn = lightbox.querySelector('.lightbox-close');
        closeBtn.addEventListener('click', function() {
            lightbox.classList.remove('active');
        });
        
        return lightbox;
    }
}

// Form validation
const forms = document.querySelectorAll('form');
forms.forEach(form => {
    form.addEventListener('submit', function(e) {
        const requiredFields = form.querySelectorAll('[required]');
        let isValid = true;
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.classList.add('error');
                
                if (!field.nextElementSibling || !field.nextElementSibling.classList.contains('error-message')) {
                    const errorMsg = document.createElement('div');
                    errorMsg.className = 'error-message';
                    errorMsg.textContent = 'Este campo é obrigatório';
                    field.parentNode.insertBefore(errorMsg, field.nextSibling);
                }
            } else {
                field.classList.remove('error');
                if (field.nextElementSibling && field.nextElementSibling.classList.contains('error-message')) {
                    field.nextElementSibling.remove();
                }
            }
        });
        
        if (!isValid) {
            e.preventDefault();
        }
    });
});

// Add error styles
const errorStyle = document.createElement('style');
errorStyle.innerHTML = `
    .error {
        border-color: var(--danger-color) !important;
    }
    
    .error-message {
        color: var(--danger-color);
        font-size: 0.8rem;
        margin-top: 0.25rem;
    }
`;
document.head.appendChild(errorStyle); 