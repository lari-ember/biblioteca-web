/**
 * Navigation Management Script
 * Gerencia indicador visual e estados ativos da navegação
 * Compatível com nova estrutura HTML semântica
 */

class NavigationManager {
    constructor() {
        this.navigation = document.querySelector('.navigation');
        this.indicator = document.querySelector('.indicator');
        this.navItems = document.querySelectorAll('.navigation ul li');
        this.mobileNavItems = document.querySelectorAll('.mobile-nav ul li');

        if (this.navigation) {
            this.init();
        }
    }

    init() {
        this.setupDesktopNavigation();
        this.setupMobileNavigation();
        this.setInitialActiveState();
        this.setupKeyboardNavigation();
    }

    /**
     * Configura navegação desktop
     */
    setupDesktopNavigation() {
        this.navItems.forEach((item, index) => {
            const link = item.querySelector('a');

            if (link) {
                // Click handler
                link.addEventListener('click', (e) => {
                    // Se for link externo, não interferir
                    if (link.hasAttribute('target') && link.getAttribute('target') === '_blank') {
                        return;
                    }

                    this.setActiveItem(index);
                    this.moveIndicator(index);
                });

                // Hover handlers para preview
                item.addEventListener('mouseenter', () => {
                    this.moveIndicator(index);
                });

                item.addEventListener('mouseleave', () => {
                    this.resetIndicatorToActive();
                });

                // Focus handlers para acessibilidade
                link.addEventListener('focus', () => {
                    this.moveIndicator(index);
                });

                link.addEventListener('blur', () => {
                    this.resetIndicatorToActive();
                });
            }
        });
    }

    /**
     * Configura navegação mobile
     */
    setupMobileNavigation() {
        this.mobileNavItems.forEach((item, index) => {
            const link = item.querySelector('a');

            if (link) {
                link.addEventListener('click', (e) => {
                    // Remove active de todos
                    this.mobileNavItems.forEach(navItem => {
                        navItem.querySelector('a').removeAttribute('aria-current');
                    });

                    // Adiciona active ao clicado (se não for externo)
                    if (!link.hasAttribute('target') || link.getAttribute('target') !== '_blank') {
                        link.setAttribute('aria-current', 'page');
                    }
                });
            }
        });
    }

    /**
     * Define estado inicial baseado na URL atual
     */
    setInitialActiveState() {
        const currentPath = window.location.pathname;
        let activeIndex = 0;

        // Mapear URLs para índices
        const urlMap = {
            '/': 0,
            '/home': 0,
            '/register_new_book': 1,
            '/your_collection': 2,
            '/search': 3,
            '/about_your_library': 4,
            '/profile': 6,
            '/login': 7,
            '/logout': 7
        };

        // Encontrar índice ativo
        if (urlMap.hasOwnProperty(currentPath)) {
            activeIndex = urlMap[currentPath];
        }

        // Definir item ativo
        this.setActiveItem(activeIndex);
        this.moveIndicator(activeIndex, false); // sem animação inicial
    }

    /**
     * Define item ativo
     */
    setActiveItem(index) {
        // Remove aria-current de todos
        this.navItems.forEach(item => {
            const link = item.querySelector('a');
            if (link) {
                link.removeAttribute('aria-current');
            }
        });

        // Adiciona aria-current ao item ativo
        if (this.navItems[index]) {
            const activeLink = this.navItems[index].querySelector('a');
            if (activeLink && (!activeLink.hasAttribute('target') || activeLink.getAttribute('target') !== '_blank')) {
                activeLink.setAttribute('aria-current', 'page');
            }
        }

        // Salvar no localStorage
        localStorage.setItem('activeNavIndex', index.toString());
    }

    /**
     * Move indicador para posição específica
     */
    moveIndicator(index, animated = true) {
        if (!this.indicator) return;

        const translateX = index * 70; // 70px por item

        if (!animated) {
            this.indicator.style.transition = 'none';
        }

        this.indicator.style.transform = `translateX(${translateX}px)`;

        if (!animated) {
            // Restaurar transição após um frame
            requestAnimationFrame(() => {
                this.indicator.style.transition = '';
            });
        }
    }

    /**
     * Retorna indicador para item ativo
     */
    resetIndicatorToActive() {
        const activeIndex = parseInt(localStorage.getItem('activeNavIndex') || '0');
        this.moveIndicator(activeIndex);
    }

    /**
     * Configuração de navegação por teclado
     */
    setupKeyboardNavigation() {
        document.addEventListener('keydown', (e) => {
            const activeElement = document.activeElement;

            // Se estiver focado em um link da navegação
            if (activeElement && activeElement.closest('.navigation ul li')) {
                const currentItem = activeElement.closest('li');
                const currentIndex = Array.from(this.navItems).indexOf(currentItem);
                let nextIndex = currentIndex;

                switch(e.key) {
                    case 'ArrowLeft':
                        e.preventDefault();
                        nextIndex = currentIndex > 0 ? currentIndex - 1 : this.navItems.length - 1;
                        break;
                    case 'ArrowRight':
                        e.preventDefault();
                        nextIndex = currentIndex < this.navItems.length - 1 ? currentIndex + 1 : 0;
                        break;
                    case 'Home':
                        e.preventDefault();
                        nextIndex = 0;
                        break;
                    case 'End':
                        e.preventDefault();
                        nextIndex = this.navItems.length - 1;
                        break;
                }

                if (nextIndex !== currentIndex) {
                    const nextLink = this.navItems[nextIndex]?.querySelector('a');
                    if (nextLink) {
                        nextLink.focus();
                        this.moveIndicator(nextIndex);
                    }
                }
            }
        });
    }

    /**
     * Método público para definir item ativo externamente
     */
    setActive(index) {
        this.setActiveItem(index);
        this.moveIndicator(index);
    }

    /**
     * Método público para obter item ativo atual
     */
    getActiveIndex() {
        return parseInt(localStorage.getItem('activeNavIndex') || '0');
    }
}

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    window.navigationManager = new NavigationManager();
});

// Exportar para uso em outros scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = NavigationManager;
}
