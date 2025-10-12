/**
 * Card Interactions Manager
 * Gerencia todas as interações dos novos componentes de card
 * Seguindo especificações do relatório cards-articles-redesign-2025-09-29
 */

class CardManager {
    constructor() {
        this.cards = document.querySelectorAll('.card[data-href]');
        this.init();
    }

    init() {
        this.setupCardInteractions();
        this.setupKeyboardNavigation();
        this.setupAccessibilityEnhancements();
        this.setupLoadingStates();
    }

    /**
     * Configura interações básicas dos cards
     */
    setupCardInteractions() {
        this.cards.forEach(card => {
            // Click handler para cards clicáveis
            card.addEventListener('click', (e) => {
                // Não ativar se clicou diretamente no CTA
                if (e.target.closest('.card-cta')) {
                    return;
                }

                const href = card.dataset.href;
                if (href) {
                    // Adiciona efeito de loading
                    this.showLoadingState(card);

                    // Navega após pequeno delay para mostrar feedback visual
                    setTimeout(() => {
                        window.location.href = href;
                    }, 150);
                }
            });

            // Hover effects com suporte a reduced motion
            card.addEventListener('mouseenter', () => {
                this.animateCard(card, true);
            });

            card.addEventListener('mouseleave', () => {
                this.animateCard(card, false);
            });

            // Focus management
            card.addEventListener('focus', () => {
                this.animateCard(card, true);
                this.announceCardFocus(card);
            });

            card.addEventListener('blur', () => {
                this.animateCard(card, false);
            });
        });
    }

    /**
     * Configura navegação por teclado avançada
     */
    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            const activeCard = document.activeElement;

            if (activeCard && activeCard.classList.contains('card')) {
                switch(e.key) {
                    case 'Enter':
                    case ' ':
                        e.preventDefault();
                        activeCard.click();
                        break;

                    case 'ArrowRight':
                        e.preventDefault();
                        this.focusNextCard(activeCard);
                        break;

                    case 'ArrowLeft':
                        e.preventDefault();
                        this.focusPreviousCard(activeCard);
                        break;

                    case 'ArrowDown':
                        e.preventDefault();
                        this.focusCardBelow(activeCard);
                        break;

                    case 'ArrowUp':
                        e.preventDefault();
                        this.focusCardAbove(activeCard);
                        break;

                    case 'Home':
                        e.preventDefault();
                        this.focusFirstCard();
                        break;

                    case 'End':
                        e.preventDefault();
                        this.focusLastCard();
                        break;
                }
            }
        });
    }

    /**
     * Move foco para próximo card
     */
    focusNextCard(currentCard) {
        const allCards = Array.from(this.cards);
        const currentIndex = allCards.indexOf(currentCard);
        const nextIndex = (currentIndex + 1) % allCards.length;
        allCards[nextIndex].focus();
    }

    /**
     * Move foco para card anterior
     */
    focusPreviousCard(currentCard) {
        const allCards = Array.from(this.cards);
        const currentIndex = allCards.indexOf(currentCard);
        const previousIndex = currentIndex === 0 ? allCards.length - 1 : currentIndex - 1;
        allCards[previousIndex].focus();
    }

    /**
     * Move foco para card abaixo (considerando grid 2x2)
     */
    focusCardBelow(currentCard) {
        const allCards = Array.from(this.cards);
        const currentIndex = allCards.indexOf(currentCard);
        const belowIndex = currentIndex + 2;

        if (belowIndex < allCards.length) {
            allCards[belowIndex].focus();
        }
    }

    /**
     * Move foco para card acima (considerando grid 2x2)
     */
    focusCardAbove(currentCard) {
        const allCards = Array.from(this.cards);
        const currentIndex = allCards.indexOf(currentCard);
        const aboveIndex = currentIndex - 2;

        if (aboveIndex >= 0) {
            allCards[aboveIndex].focus();
        }
    }

    /**
     * Move foco para primeiro card
     */
    focusFirstCard() {
        if (this.cards.length > 0) {
            this.cards[0].focus();
        }
    }

    /**
     * Move foco para último card
     */
    focusLastCard() {
        if (this.cards.length > 0) {
            this.cards[this.cards.length - 1].focus();
        }
    }

    /**
     * Anima card com verificação de reduced motion
     */
    animateCard(card, isActive) {
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (!prefersReducedMotion) {
            if (isActive) {
                card.style.transform = 'translateY(-4px)';
                card.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.4)';
            } else {
                card.style.transform = '';
                card.style.boxShadow = '';
            }
        }
    }

    /**
     * Anuncia foco do card para screen readers
     */
    announceCardFocus(card) {
        const title = card.querySelector('.card-title')?.textContent;
        const eyebrow = card.querySelector('.card-eyebrow')?.textContent;
        const description = card.querySelector('.card-desc')?.textContent;

        if (title) {
            const announcement = `${eyebrow ? eyebrow + ': ' : ''}${title}. ${description ? description.substring(0, 100) + '...' : ''} Pressione Enter para ativar.`;
            this.announceToScreenReader(announcement);
        }
    }

    /**
     * Configura melhorias de acessibilidade
     */
    setupAccessibilityEnhancements() {
        // Configura região para anúncios dinâmicos
        if (!document.getElementById('card-announcements')) {
            const announcer = document.createElement('div');
            announcer.id = 'card-announcements';
            announcer.setAttribute('aria-live', 'polite');
            announcer.setAttribute('aria-atomic', 'true');
            announcer.className = 'sr-only';
            document.body.appendChild(announcer);
        }

        // Melhora labels dos cards
        this.cards.forEach((card, index) => {
            const title = card.querySelector('.card-title')?.textContent || `Card ${index + 1}`;
            const eyebrow = card.querySelector('.card-eyebrow')?.textContent;

            if (!card.hasAttribute('aria-label')) {
                const label = `${eyebrow ? eyebrow + ': ' : ''}${title} - Pressione Enter para ativar`;
                card.setAttribute('aria-label', label);
            }

            // Garante que o card é focável
            if (!card.hasAttribute('tabindex')) {
                card.setAttribute('tabindex', '0');
            }
        });
    }

    /**
     * Configura estados de loading
     */
    setupLoadingStates() {
        // Preload de imagens para melhor UX
        this.cards.forEach(card => {
            const img = card.querySelector('.card-media img');
            if (img && !img.complete) {
                img.addEventListener('load', () => {
                    card.classList.remove('card--loading');
                });

                img.addEventListener('error', () => {
                    this.handleImageError(card, img);
                });

                // Adiciona estado de loading inicial
                card.classList.add('card--loading');
            }
        });
    }

    /**
     * Mostra estado de loading no card
     */
    showLoadingState(card) {
        card.classList.add('card--loading');

        // Desabilita interações temporariamente
        card.style.pointerEvents = 'none';

        // Remove loading após timeout de segurança
        setTimeout(() => {
            this.hideLoadingState(card);
        }, 3000);
    }

    /**
     * Remove estado de loading
     */
    hideLoadingState(card) {
        card.classList.remove('card--loading');
        card.style.pointerEvents = '';
    }

    /**
     * Lida com erro de carregamento de imagem
     */
    handleImageError(card, img) {
        card.classList.remove('card--loading');

        // Substitui por placeholder ou remove imagem
        const placeholder = document.createElement('div');
        placeholder.className = 'card-media-placeholder';
        placeholder.innerHTML = '📚';
        placeholder.style.cssText = `
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 3rem;
            background: var(--color-dark);
            color: var(--color-text);
        `;

        img.parentElement.replaceChild(placeholder, img);
    }

    /**
     * Anuncia mensagens para screen readers
     */
    announceToScreenReader(message) {
        const announcer = document.getElementById('card-announcements');
        if (announcer) {
            announcer.textContent = message;

            // Limpa após um tempo
            setTimeout(() => {
                announcer.textContent = '';
            }, 1000);
        }
    }

    /**
     * Mé público para adicionar novos cards dinamicamente
     */
    addCard(cardElement) {
        if (cardElement.hasAttribute('data-href')) {
            this.cards = document.querySelectorAll('.card[data-href]');
            this.setupCardInteractions();
        }
    }

    /**
     * Mé público para obter estatísticas dos cards
     */
    getCardStats() {
        return {
            totalCards: this.cards.length,
            cardsWithImages: document.querySelectorAll('.card .card-media img').length,
            featuredCards: document.querySelectorAll('.card--featured').length,
            loadingCards: document.querySelectorAll('.card--loading').length
        };
    }
}

// Auto-inicialização quando DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    try {
        window.cardManager = new CardManager();

        // Log para debug (remover em produção)
        if (window.location.hostname === 'localhost') {
            console.log('Card Manager initialized:', window.cardManager.getCardStats());
        }
    } catch (error) {
        console.error('Erro ao inicializar Card Manager:', error);
    }
});

// Exporta para uso em outros módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CardManager;
}
