/**
 * Features Section Manager
 * Gerencia interações, navegação e acessibilidade da seção de features
 * @module FeaturesManager
 */

class FeaturesManager {
    constructor() {
        this.cards = [];
        this.currentFocusIndex = -1;
        this.liveRegion = null;
        this.init();
    }

    /**
     * Inicializa o gerenciador de features
     */
    init() {
        this.setupLiveRegion();
        this.setupCards();
        this.setupCarousel();
        this.setupIntersectionObserver();
    }

    /**
     * Cria região ARIA live para anúncios de screen reader
     */
    setupLiveRegion() {
        this.liveRegion = document.createElement('div');
        this.liveRegion.setAttribute('role', 'status');
        this.liveRegion.setAttribute('aria-live', 'polite');
        this.liveRegion.setAttribute('aria-atomic', 'true');
        this.liveRegion.className = 'sr-only';
        document.body.appendChild(this.liveRegion);
    }

    /**
     * Configura cards com navegação e interatividade
     */
    setupCards() {
        this.cards = Array.from(document.querySelectorAll('.card[tabindex]'));

        this.cards.forEach((card, index) => {
            // Navegação por clique
            if (card.hasAttribute('data-href')) {
                card.addEventListener('click', (e) => this.handleCardClick(e, card));
            }

            // Navegação por teclado
            card.addEventListener('keydown', (e) => this.handleCardKeydown(e, card, index));

            // Foco visual
            card.addEventListener('focus', () => this.handleCardFocus(card, index));
        });
    }

    /**
     * Gerencia clique em card
     */
    handleCardClick(event, card) {
        // Previne navegação se clicou no CTA interno
        if (event.target.closest('.card-cta')) {
            return;
        }

        const href = card.getAttribute('data-href');
        if (href) {
            window.location.href = href;
        }
    }

    /**
     * Gerencia navegação por teclado em cards
     */
    handleCardKeydown(event, card, index) {
        const key = event.key;

        // Enter ou Space: ativa o card
        if (key === 'Enter' || key === ' ') {
            event.preventDefault();
            const href = card.getAttribute('data-href');
            if (href) {
                window.location.href = href;
            }
            return;
        }

        // Navegação por setas
        let targetIndex = index;

        switch(key) {
            case 'ArrowRight':
            case 'ArrowDown':
                event.preventDefault();
                targetIndex = (index + 1) % this.cards.length;
                break;
            case 'ArrowLeft':
            case 'ArrowUp':
                event.preventDefault();
                targetIndex = (index - 1 + this.cards.length) % this.cards.length;
                break;
            case 'Home':
                event.preventDefault();
                targetIndex = 0;
                break;
            case 'End':
                event.preventDefault();
                targetIndex = this.cards.length - 1;
                break;
            default:
                return;
        }

        // Move foco para o card alvo
        this.cards[targetIndex].focus();
    }

    /**
     * Gerencia foco em card
     */
    handleCardFocus(card, index) {
        this.currentFocusIndex = index;

        // Anuncia card para screen readers
        const title = card.querySelector('.card-title');
        const eyebrow = card.querySelector('.card-eyebrow');

        if (title && eyebrow) {
            this.announce(`${eyebrow.textContent}: ${title.textContent}. Card ${index + 1} de ${this.cards.length}`);
        }
    }

    /**
     * Configura carrossel de livros em destaque (se existir)
     */
    setupCarousel() {
        const carousel = document.querySelector('.books-carousel');
        if (!carousel) return;

        const track = carousel.querySelector('.books-carousel__track');
        if (!track) return;

        // Adiciona suporte a scroll com teclado
        track.setAttribute('tabindex', '0');
        track.setAttribute('role', 'region');
        track.setAttribute('aria-label', 'Carrossel de livros em destaque');

        track.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight') {
                track.scrollBy({ left: 220, behavior: 'smooth' });
            } else if (e.key === 'ArrowLeft') {
                track.scrollBy({ left: -220, behavior: 'smooth' });
            }
        });
    }

    /**
     * Configura Intersection Observer para animações on-scroll
     */
    setupIntersectionObserver() {
        // Verifica preferência de movimento reduzido
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (prefersReducedMotion) return;

        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('fade-in-view');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Observa cards e seções
        document.querySelectorAll('.card, .features-header, .developer-section').forEach(el => {
            observer.observe(el);
        });
    }

    /**
     * Anuncia mensagem para screen readers
     */
    announce(message) {
        if (this.liveRegion) {
            this.liveRegion.textContent = message;

            // Limpa após 1 segundo
            setTimeout(() => {
                this.liveRegion.textContent = '';
            }, 1000);
        }
    }

    /**
     * Destrói o gerenciador e remove event listeners
     */
    destroy() {
        this.cards.forEach(card => {
            card.replaceWith(card.cloneNode(true));
        });

        if (this.liveRegion && this.liveRegion.parentNode) {
            this.liveRegion.parentNode.removeChild(this.liveRegion);
        }
    }
}

/**
 * Book Highlights Manager
 * Gerencia a seção de livros em destaque
 */
class BookHighlightsManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupBookCards();
        this.setupLazyLoading();
    }

    /**
     * Configura interações de cards de livros
     */
    setupBookCards() {
        const bookCards = document.querySelectorAll('.book-highlight-card');

        bookCards.forEach(card => {
            card.setAttribute('tabindex', '0');
            card.setAttribute('role', 'article');

            // Torna card clicável se tiver link
            const link = card.querySelector('a');
            if (link) {
                card.style.cursor = 'pointer';

                card.addEventListener('click', (e) => {
                    if (!e.target.closest('a')) {
                        link.click();
                    }
                });

                card.addEventListener('keydown', (e) => {
                    if (e.key === 'Enter' || e.key === ' ') {
                        e.preventDefault();
                        link.click();
                    }
                });
            }
        });
    }

    /**
     * Configura lazy loading de imagens de livros
     */
    setupLazyLoading() {
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        if (img.dataset.src) {
                            img.src = img.dataset.src;
                            img.removeAttribute('data-src');
                        }
                        observer.unobserve(img);
                    }
                });
            });

            document.querySelectorAll('.book-highlight-card__cover img[data-src]').forEach(img => {
                imageObserver.observe(img);
            });
        }
    }
}

/**
 * Inicialização quando DOM estiver pronto
 */
document.addEventListener('DOMContentLoaded', () => {
    // Inicializa gerenciador de features
    const featuresManager = new FeaturesManager();

    // Inicializa gerenciador de livros em destaque (se existir)
    if (document.querySelector('.featured-books-section')) {
        const bookHighlightsManager = new BookHighlightsManager();
    }

    // Expõe globalmente para debug
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
        window.featuresManager = featuresManager;
    }
});

// Exporta para uso em módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { FeaturesManager, BookHighlightsManager };
}

