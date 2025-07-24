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
                text: "Excelente profissional, muito atencioso e prestativo. Resolveu minha documentação com rapidez e eficiência. Recomendo a todos! Melhor despachante do Rio de Janeiro.",
                name: "Marcos Paulo",
                photo: "https://lh3.googleusercontent.com/a/ACg8ocLXBhCkvHG9T8rHMJ_oH-Ka_8Qd8YHUYl9ZtJWxQMY=s40-c-rp-mo-br100",
                rating: 5
            },
            {
                text: "Profissional extremamente competente e atencioso. Resolveu minha documentação com rapidez e eficiência. Super recomendo!",
                name: "Ana Carolina Silva",
                photo: "https://lh3.googleusercontent.com/a/ACg8ocLXBhCkvHG9T8rHMJ_oH-Ka_8Qd8YHUYl9ZtJWxQMY=s40-c-rp-mo-br100",
                rating: 5
            },
            {
                text: "Ótimo profissional, muito atencioso e prestativo. Resolveu tudo com muita agilidade e competência. Recomendo!",
                name: "Ricardo Santos",
                photo: "https://lh3.googleusercontent.com/a/ACg8ocLXBhCkvHG9T8rHMJ_oH-Ka_8Qd8YHUYl9ZtJWxQMY=s40-c-rp-mo-br100",
                rating: 5
            },
            {
                text: "Serviço de primeira qualidade! O Wellington é muito profissional e atencioso. Resolveu minha documentação de forma rápida e eficiente.",
                name: "Pedro Henrique Costa",
                photo: "https://lh3.googleusercontent.com/a/ACg8ocLXBhCkvHG9T8rHMJ_oH-Ka_8Qd8YHUYl9ZtJWxQMY=s40-c-rp-mo-br100",
                rating: 5
            },
            {
                text: "Melhor despachante do Rio! Atendimento nota 10, super profissional e eficiente. Resolveu minha documentação sem burocracia.",
                name: "Fernanda Lima",
                photo: "https://lh3.googleusercontent.com/a/ACg8ocLXBhCkvHG9T8rHMJ_oH-Ka_8Qd8YHUYl9ZtJWxQMY=s40-c-rp-mo-br100",
                rating: 5
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
                        <img src="${review.photo}" alt="${review.name}" class="w-12 h-12 rounded-full object-cover">
                        <div class="ml-3">
                            <p class="font-medium">${review.name}</p>
                            <p class="text-sm text-gray-500">★ ${review.rating}.0</p>
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
        
        if (!slider || !prevButton || !nextButton || !dotsContainer) return;
        
        const testimonials = slider.children;
        const totalTestimonials = testimonials.length;
        let currentIndex = 0;
        
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
            currentIndex = Math.min(currentIndex + slidesPerView, totalTestimonials - slidesPerView);
            updateSliderPosition();
        }
        
        function prevSlide() {
            const slidesPerView = window.innerWidth >= 1024 ? 3 : 1;
            currentIndex = Math.max(currentIndex - slidesPerView, 0);
            updateSliderPosition();
        }
        
        prevButton.addEventListener('click', prevSlide);
        nextButton.addEventListener('click', nextSlide);
        
        createDots();
        
        let autoplayInterval = setInterval(nextSlide, 5000);
        const testimonialContainer = document.getElementById('testimonials-container');
        
        if (testimonialContainer) {
            testimonialContainer.addEventListener('mouseenter', () => {
                clearInterval(autoplayInterval);
            });
            
            testimonialContainer.addEventListener('mouseleave', () => {
                autoplayInterval = setInterval(nextSlide, 5000);
            });
        }
        
        window.addEventListener('resize', () => {
            currentIndex = 0;
            createDots();
            updateSliderPosition();
        });
        
        // Inicialização inicial
        updateSliderPosition();
    }
    
    // Carregar os depoimentos
    fetchGoogleReviews();
    
    // Validação do formulário de contato
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
            // Aqui você pode adicionar o código para enviar o formulário via AJAX
            alert('Mensagem enviada com sucesso! Entraremos em contato em breve.');
            contactForm.reset();
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