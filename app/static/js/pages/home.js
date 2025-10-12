/**
 * Home Page JavaScript
 * Scripts específicos para a página inicial
 * Seguindo padrões de acessibilidade e performance
 */

class HomePage {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.initializeAnimations();
        this.setupAccessibility();
        this.initializeDateTime();
        this.setupKeyboardNavigation();
    }

    /**
     * Configura os event listeners da página
     */
    setupEventListeners() {
        document.addEventListener('DOMContentLoaded', () => {
            this.initNavigationActive();
            this.setupSmoothScrolling();
            this.setupFeatureCardInteractions();
        });

        // Listener para mudanças de tema/contraste
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', this.handleThemeChange.bind(this));
            window.matchMedia('(prefers-reduced-motion: reduce)').addEventListener('change', this.handleMotionPreference.bind(this));
        }
    }

    /**
     * Configuração de navegação por teclado para acessibilidade
     */
    setupKeyboardNavigation() {
        // Ativação de cards por teclado
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                const activeElement = document.activeElement;

                // Se o elemento ativo é um feature-card com data-href
                if (activeElement && activeElement.classList.contains('feature-card') && activeElement.dataset.href) {
                    e.preventDefault();
                    window.location.href = activeElement.dataset.href;
                    return;
                }

                // Se o elemento ativo é um card focável genérico
                if (activeElement && activeElement.classList.contains('feature-card')) {
                    e.preventDefault();
                    const button = activeElement.querySelector('.btn');
                    if (button) {
                        button.click();
                    }
                }
            }
        });

        // Melhorar navegação por setas (opcional)
        document.addEventListener('keydown', (e) => {
            const activeElement = document.activeElement;

            if (activeElement && activeElement.classList.contains('feature-card')) {
                let nextElement = null;

                switch(e.key) {
                    case 'ArrowRight':
                        nextElement = activeElement.nextElementSibling;
                        break;
                    case 'ArrowLeft':
                        nextElement = activeElement.previousElementSibling;
                        break;
                    case 'ArrowDown':
                        // Próxima linha no grid
                        const currentIndex = Array.from(activeElement.parentNode.children).indexOf(activeElement);
                        const nextRowElement = activeElement.parentNode.children[currentIndex + 2];
                        if (nextRowElement) nextElement = nextRowElement;
                        break;
                    case 'ArrowUp':
                        // Linha anterior no grid
                        const currentIdx = Array.from(activeElement.parentNode.children).indexOf(activeElement);
                        const prevRowElement = activeElement.parentNode.children[currentIdx - 2];
                        if (prevRowElement) nextElement = prevRowElement;
                        break;
                }

                if (nextElement && nextElement.classList.contains('feature-card')) {
                    e.preventDefault();
                    nextElement.focus();
                }
            }
        });
    }

    /**
     * Inicializa animações com suporte a preferências de acessibilidade
     */
    initializeAnimations() {
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (!prefersReducedMotion) {
            this.setupScrollAnimations();
            this.setupParallaxEffects();
        }
    }

    /**
     * Configurações de acessibilidade
     */
    setupAccessibility() {
        // Adiciona skip links para navegação por teclado
        this.addSkipLinks();

        // Configura ARIA labels dinâmicos
        this.setupAriaLabels();

        // Gerencia foco para usuários de teclado
        this.setupFocusManagement();

        // Configura anúncios para screen readers
        this.setupScreenReaderAnnouncements();
    }

    /**
     * Gerencia a navegação ativa com persistência
     */
    initNavigationActive() {
        const navigationItems = document.querySelectorAll('.navigation .list');
        const currentPath = window.location.pathname;

        // Remove todas as classes active
        navigationItems.forEach(item => item.classList.remove('active'));

        // Adiciona active baseado na URL atual
        navigationItems.forEach((item, index) => {
            const link = item.querySelector('a');
            if (link && (link.getAttribute('href') === currentPath ||
                        (currentPath === '/' && link.getAttribute('href') === '/home'))) {
                item.classList.add('active');
                localStorage.setItem('activeNavIndex', index.toString());
            }
        });

        // Event listeners para navegação
        navigationItems.forEach((item, index) => {
            item.addEventListener('click', () => {
                navigationItems.forEach(nav => nav.classList.remove('active'));
                item.classList.add('active');
                localStorage.setItem('activeNavIndex', index.toString());
            });

            // Suporte a navegação por teclado
            item.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    item.querySelector('a').click();
                }
            });
        });
    }

    /**
     * Configura scroll suave para âncoras
     */
    setupSmoothScrolling() {
        const links = document.querySelectorAll('a[href^="#"]');

        links.forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const targetId = link.getAttribute('href').substring(1);
                const targetElement = document.getElementById(targetId);

                if (targetElement) {
                    targetElement.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });

                    // Gerencia foco para acessibilidade
                    targetElement.focus();

                    // Anuncia mudança para screen readers
                    this.announceToScreenReader(`Navegando para ${targetElement.textContent || targetId}`);
                }
            });
        });
    }

    /**
     * Adiciona interações aos cards de funcionalidades
     */
    setupFeatureCardInteractions() {
        const featureCards = document.querySelectorAll('.feature-card');

        featureCards.forEach(card => {
            // Event listeners para hover/focus
            card.addEventListener('mouseenter', () => this.animateCard(card, true));
            card.addEventListener('mouseleave', () => this.animateCard(card, false));
            card.addEventListener('focus', () => {
                this.animateCard(card, true);
                this.announceCardFocus(card);
            });
            card.addEventListener('blur', () => this.animateCard(card, false));
        });
    }

    /**
     * Anuncia foco do card para screen readers
     */
    announceCardFocus(card) {
        const title = card.querySelector('h3')?.textContent;
        const description = card.querySelector('p')?.textContent;
        if (title) {
            this.announceToScreenReader(`Focado em ${title}. ${description ? description.substring(0, 100) + '...' : ''} Pressione Enter para ativar.`);
        }
    }

    /**
     * Anima cards com verificação de preferências de movimento
     */
    animateCard(card, isActive) {
        const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (!prefersReducedMotion) {
            if (isActive) {
                card.style.transform = 'translateY(-10px)';
                card.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.34)';
            } else {
                card.style.transform = 'translateY(0)';
                card.style.boxShadow = '';
            }
        }
    }

    /**
     * Configura animações baseadas em scroll
     */
    setupScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        // Observa elementos que devem animar
        const animatedElements = document.querySelectorAll('.feature-card, .about-content, .hero-content');
        animatedElements.forEach(el => {
            observer.observe(el);
        });
    }

    /**
     * Configura efeitos de parallax sutis
     */
    setupParallaxEffects() {
        const heroImage = document.querySelector('.hero-image');

        if (heroImage) {
            window.addEventListener('scroll', () => {
                const scrolled = window.pageYOffset;
                const rate = scrolled * -0.2; // Reduzido para ser mais sutil

                heroImage.style.transform = `translateY(${rate}px)`;
            });
        }
    }

    /**
     * Inicializa e gerencia data/hora
     */
    initializeDateTime() {
        this.updateDateTime();

        // Atualiza a cada minuto
        setInterval(() => {
            this.updateDateTime();
        }, 60000);
    }

    /**
     * Atualiza elementos de data e hora
     */
    updateDateTime() {
        const now = new Date();

        // Atualiza data
        const dateElement = document.getElementById('date');
        if (dateElement) {
            const options = {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                weekday: 'long'
            };
            dateElement.textContent = now.toLocaleDateString('pt-BR', options);
            dateElement.setAttribute('datetime', now.toISOString().split('T')[0]);
        }

        // Atualiza hora
        const timeElement = document.querySelector('time');
        if (timeElement) {
            const timeString = now.toLocaleTimeString('pt-BR', {
                hour: '2-digit',
                minute: '2-digit'
            });
            timeElement.textContent = timeString;
            timeElement.setAttribute('datetime', now.toISOString());
        }
    }

    /**
     * Adiciona skip links para navegação por teclado
     */
    addSkipLinks() {
        // Skip link já adicionado via CSS em base.css
        // Aqui podemos adicionar comportamentos adicionais se necessário
        const skipLinks = document.querySelectorAll('.skip-link');
        skipLinks.forEach(link => {
            link.addEventListener('click', (e) => {
                const targetId = link.getAttribute('href').substring(1);
                const target = document.getElementById(targetId);
                if (target) {
                    target.setAttribute('tabindex', '-1');
                    target.focus();
                    target.addEventListener('blur', () => {
                        target.removeAttribute('tabindex');
                    }, { once: true });
                }
            });
        });
    }

    /**
     * Configura ARIA labels dinâmicos
     */
    setupAriaLabels() {
        // Adiciona labels para elementos interativos
        const featureCards = document.querySelectorAll('.feature-card');
        featureCards.forEach((card, index) => {
            const title = card.querySelector('h3')?.textContent || `Funcionalidade ${index + 1}`;
            if (!card.hasAttribute('aria-label')) {
                card.setAttribute('aria-label', `${title} - Pressione Enter para acessar`);
            }
        });

        // Adiciona descrições para imagens decorativas
        const decorativeImages = document.querySelectorAll('.hero-image, .about-image');
        decorativeImages.forEach(img => {
            if (!img.hasAttribute('aria-hidden')) {
                img.setAttribute('aria-hidden', 'true');
            }
            if (!img.hasAttribute('alt')) {
                img.setAttribute('alt', '');
            }
        });
    }

    /**
     * Gerencia foco para melhor acessibilidade
     */
    setupFocusManagement() {
        // Adiciona outline visível para elementos focáveis
        const focusableElements = document.querySelectorAll('a, button, .feature-card, .navigation .list');

        focusableElements.forEach(element => {
            element.addEventListener('focus', () => {
                element.classList.add('focused');
            });

            element.addEventListener('blur', () => {
                element.classList.remove('focused');
            });
        });
    }

    /**
     * Configura anúncios para screen readers
     */
    setupScreenReaderAnnouncements() {
        // Cria região para anúncios dinâmicos
        if (!document.getElementById('sr-announcements')) {
            const announcer = document.createElement('div');
            announcer.id = 'sr-announcements';
            announcer.setAttribute('aria-live', 'polite');
            announcer.setAttribute('aria-atomic', 'true');
            announcer.className = 'sr-only';
            document.body.appendChild(announcer);
        }
    }

    /**
     * Anuncia mensagens para screen readers
     */
    announceToScreenReader(message) {
        const announcer = document.getElementById('sr-announcements');
        if (announcer) {
            announcer.textContent = message;
            // Limpa depois de um tempo
            setTimeout(() => {
                announcer.textContent = '';
            }, 1000);
        }
    }

    /**
     * Lida com mudanças de tema
     */
    handleThemeChange(e) {
        const theme = e.matches ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', theme);
        this.announceToScreenReader(`Tema alterado para ${theme === 'dark' ? 'escuro' : 'claro'}`);
    }

    /**
     * Lida com preferências de movimento
     */
    handleMotionPreference(e) {
        if (e.matches) {
            // Desabilita animações
            document.body.style.setProperty('--animation-duration', '0s');
            this.announceToScreenReader('Animações reduzidas');
        } else {
            // Habilita animações
            document.body.style.removeProperty('--animation-duration');
            this.announceToScreenReader('Animações habilitadas');
        }
    }

    /**
     * Mé utilitário para log de erros
     */
    logError(error, context) {
        console.error(`Erro na página inicial [${context}]:`, error);

        // Em produção, você pode enviar para um serviço de monitoramento
        if (window.errorReporting) {
            window.errorReporting.captureException(error, { context });
        }
    }
}

// Inicializa a classe quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', () => {
    try {
        new HomePage();
    } catch (error) {
        console.error('Erro ao inicializar página inicial:', error);
    }
});

// Exporta para uso em outros módulos se necessário
if (typeof module !== 'undefined' && module.exports) {
    module.exports = HomePage;
}
