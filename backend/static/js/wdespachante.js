/* Scripts para a página principal wdespachante.com.br */

// JavaScript para funcionalidade do FAQ
document.querySelectorAll('.faq-question').forEach(item => {
    item.addEventListener('click', event => {
        const faqItem = item.closest('.faq-item');
        faqItem.classList.toggle('active');
    });
});

// JavaScript para o slider de depoimentos
const slidesWrapper = document.querySelector('.slides-wrapper');
const testimonialCards = document.querySelectorAll('.testimonial-card');
const sliderNav = document.querySelector('.slider-nav');
const totalSlides = testimonialCards.length;
let currentIndex = 0;

if (totalSlides > 0) {
    // Criar dots de navegação
    for (let i = 0; i < totalSlides; i++) {
        const dot = document.createElement('span');
        dot.classList.add('dot');
        dot.dataset.index = i;
        dot.addEventListener('click', () => {
            moveToSlide(parseInt(dot.dataset.index));
        });
        sliderNav.appendChild(dot);
    }

    const dots = document.querySelectorAll('.dot');

    function moveToSlide(index) {
        if (index >= totalSlides) currentIndex = 0;
        else if (index < 0) currentIndex = totalSlides - 1;
        else currentIndex = index;

        slidesWrapper.style.transform = `translateX(${-currentIndex * testimonialCards[0].clientWidth}px)`;

        dots.forEach((dot, i) => {
            if (i === currentIndex) {
                dot.classList.add('active');
            } else {
                dot.classList.remove('active');
            }
        });
    }

    // Ajustar slider em resize
    window.addEventListener('resize', () => {
        slidesWrapper.style.transition = 'none'; // Desabilita transição durante resize
        slidesWrapper.style.transform = `translateX(${-currentIndex * testimonialCards[0].clientWidth}px)`;
        setTimeout(() => {
            slidesWrapper.style.transition = 'transform 0.5s ease-in-out'; // Reabilita transição
        }, 50);
    });

    moveToSlide(0);
}

// Filtro de Detrans (muito básico, pode ser melhorado com backend ou mais complexidade JS)
const detranSearchInput = document.getElementById('detran-search-input');
const detransListContainer = document.getElementById('detrans-list');
const originalDetranCards = Array.from(detransListContainer.children); // Captura os elementos originais

detranSearchInput.addEventListener('input', function() {
    const searchTerm = this.value.toLowerCase();
    detransListContainer.innerHTML = ''; // Limpa a lista atual

    const filteredDetrans = originalDetranCards.filter(card => {
        const stateName = card.querySelector('.state-name').textContent.toLowerCase();
        const detranLink = card.querySelector('.detran-link').textContent.toLowerCase();
        return stateName.includes(searchTerm) || detranLink.includes(searchTerm);
    });

    if (filteredDetrans.length > 0) {
        filteredDetrans.forEach(card => detransListContainer.appendChild(card.cloneNode(true))); // Adiciona clones
    } else {
        detransListContainer.innerHTML = '<p style="text-align: center; color: var(--dark-gray);">Nenhum Detran encontrado com este termo. Tente outra busca.</p>';
    }
}); 