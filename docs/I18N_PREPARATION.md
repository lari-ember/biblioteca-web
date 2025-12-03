# 🌍 Internacionalização (i18n) - Documentação de Preparação

## Status Atual
**Fase 1 - Bilíngue Estático (pt-BR/en)**

O Amber Archivily atualmente utiliza uma abordagem bilíngue estática com strings em português brasileiro (pt-BR) como idioma principal e termos técnicos em inglês onde apropriado.

## Arquitetura Atual

### Strings Hardcoded Principais

#### Templates (`app/templates/`)

**index.html:**
- ✅ Marcação i18n adicionada no topo do arquivo
- Strings extraíveis:
  - Hero title: "Amber Archivily"
  - Hero subtitle: "Um grimório digital encantado..."
  - CTAs: "Adentrar o Reino dos Livros", "Iniciar Ritual ✨", etc.
  - Feature descriptions (authenticated/unauthenticated)

**base.html:**
- Meta tags dinâmicas (SEO)
- Navigation labels: "Início", "Novo Livro", "Sua Coleção", "Pesquisar", "Estatísticas"
- Footer links

**Outros templates:**
- Flash messages
- Form labels e placeholders
- Error messages

#### Controllers (`app/controllers/`)

**routes.py:**
- Flash messages: `flash('Livro adicionado com sucesso!', 'success')`
- Error messages
- Validation messages

**auth.py:**
- Login/logout messages
- Registration validation

**books.py:**
- CRUD operation messages
- Search result messages

#### Models (`app/models/`)

**modelsdb.py:**
- Validation error messages (ValueError strings)

### Filtros Jinja2 Customizados

**Filtro `timeago` (`app/__init__.py`):**
```python
# Strings pt-BR a extrair:
- "Nunca"
- "No futuro"
- "Há poucos segundos"
- "Há 1 minuto" / "Há X minutos"
- "Há 1 hora" / "Há X horas"
- "Há 1 dia" / "Há X dias"
- "Há 1 semana" / "Há X semanas"
- "Há 1 mês" / "Há X meses"
- "Há 1 ano" / "Há X anos"
```

**Filtro `datetime_br`:**
```python
# Meses em português:
meses = {
    1: 'janeiro', 2: 'fevereiro', 3: 'março', 4: 'abril',
    5: 'maio', 6: 'junho', 7: 'julho', 8: 'agosto',
    9: 'setembro', 10: 'outubro', 11: 'novembro', 12: 'dezembro'
}
```

## Plano de Migração Flask-Babel (Fase 2)

### 1. Instalação e Setup

```bash
pip install Flask-Babel
```

**`app/__init__.py`:**
```python
from flask_babel import Babel, lazy_gettext as _l

babel = Babel()

def create_app():
    app = Flask(__name__)
    # ...existing setup...
    
    babel.init_app(app)
    
    @babel.localeselector
    def get_locale():
        # 1. Tentar obter do usuário autenticado
        if current_user.is_authenticated:
            return current_user.locale
        # 2. Tentar obter da sessão
        return session.get('locale', request.accept_languages.best_match(['pt', 'en']))
    
    return app
```

### 2. Estrutura de Diretórios

```
biblioteca-web/
├── babel.cfg                 # Configuração de extração
├── translations/
│   ├── pt_BR/
│   │   └── LC_MESSAGES/
│   │       ├── messages.po   # Strings traduzidas pt-BR
│   │       └── messages.mo   # Compilado
│   └── en/
│       └── LC_MESSAGES/
│           ├── messages.po   # Strings traduzidas en
│           └── messages.mo   # Compilado
```

### 3. Configuração babel.cfg

```ini
[python: **.py]
[jinja2: **/templates/**.html]
encoding = utf-8
```

### 4. Comandos de Extração

```bash
# Extrair strings
pybabel extract -F babel.cfg -k _l -o messages.pot .

# Inicializar catálogo pt-BR
pybabel init -i messages.pot -d translations -l pt_BR

# Inicializar catálogo en
pybabel init -i messages.pot -d translations -l en

# Atualizar após mudanças
pybabel update -i messages.pot -d translations

# Compilar traduções
pybabel compile -d translations
```

### 5. Exemplos de Conversão

#### Templates (antes → depois)

**Antes:**
```jinja2
<h1>Bem-vindo, {{ current_user.username }}</h1>
<p>Você tem {{ current_user.books|length }} livros</p>
```

**Depois:**
```jinja2
<h1>{{ _('Bem-vindo, %(username)s', username=current_user.username) }}</h1>
<p>{{ _('Você tem %(count)d livros', count=current_user.books|length) }}</p>
```

#### Controllers (antes → depois)

**Antes:**
```python
flash('Livro adicionado com sucesso!', 'success')
```

**Depois:**
```python
from flask_babel import gettext as _
flash(_('Livro adicionado com sucesso!'), 'success')
```

#### Models (antes → depois)

**Antes:**
```python
raise ValueError("ISBN inválido")
```

**Depois:**
```python
from flask_babel import lazy_gettext as _l
raise ValueError(_l("ISBN inválido"))
```

### 6. Filtros Customizados i18n

**timeago com i18n:**
```python
from flask_babel import ngettext

@app.template_filter('timeago')
def timeago_filter(date_value):
    # ...existing delta calculation...
    
    if minutes < 60:
        return ngettext(
            'Há %(num)d minuto',
            'Há %(num)d minutos',
            minutes
        ) % {'num': minutes}
    
    # Similar para horas, dias, etc.
```

### 7. Seletor de Idioma UI

**base.html:**
```html
<div class="language-selector" role="navigation" aria-label="Seletor de idioma">
    <a href="{{ url_for('set_locale', locale='pt_BR') }}" 
       {% if session.get('locale') == 'pt_BR' %}aria-current="page"{% endif %}>
        🇧🇷 PT
    </a>
    <a href="{{ url_for('set_locale', locale='en') }}"
       {% if session.get('locale') == 'en' %}aria-current="page"{% endif %}>
        🇺🇸 EN
    </a>
</div>
```

**routes.py:**
```python
@app.route('/set-locale/<locale>')
def set_locale(locale):
    if locale in ['pt_BR', 'en']:
        session['locale'] = locale
        if current_user.is_authenticated:
            current_user.locale = locale
            db.session.commit()
    return redirect(request.referrer or url_for('core.index'))
```

## Inventory de Strings a Traduzir

### Prioridade Alta (Interface Principal)

| Contexto | String pt-BR | Notas |
|----------|--------------|-------|
| Navigation | "Início", "Novo Livro", "Sua Coleção" | Menu principal |
| Actions | "Iniciar Ritual ✨", "Abrir o Cofre 📚" | CTAs principais |
| Status | "Última adição: Há 2 dias" | Dinâmico via timeago |
| Genres | Ver `code_book.py` | ~50 gêneros |

### Prioridade Média (Mensagens de Sistema)

| Contexto | String pt-BR | Local |
|----------|--------------|-------|
| Flash Success | "Livro adicionado com sucesso!" | books.py |
| Flash Error | "Erro ao adicionar livro" | books.py |
| Validation | "ISBN inválido" | modelsdb.py |

### Prioridade Baixa (Conteúdo Estático)

| Contexto | String pt-BR | Local |
|----------|--------------|-------|
| About Section | "A Crônica do Amber Archivily" | index.html |
| Footer Links | "mais projetos", "Portfólio" | base.html |
| Developer Card | "A Lenda da Lady Lari" | features_section.html |

## Considerações Especiais

### 1. Preservar Identidade do Projeto

Termos como **"Amber Archivily"**, **"Lady Lari"** e elementos de branding NÃO devem ser traduzidos.

### 2. Tom Literário/Místico

A tradução para inglês deve manter o tom literário:
- "Ritual de Catalogação" → "Cataloging Ritual" (não "Add Book")
- "Salão dos Tesouros" → "Hall of Treasures" (não "Book Collection")

### 3. Emoji e Unicode

Manter emojis consistentes em ambos idiomas:
- 📜, 📚, 🔍, 📊, ✨, 🕵️, 🔮

### 4. Pluralização

Utilizar `ngettext()` para casos como:
- "1 livro" / "X livros" → "1 book" / "X books"

### 5. Data/Hora

- pt-BR: "15 de janeiro de 2025 às 10h30"
- en: "January 15, 2025 at 10:30 AM"

Usar `format_datetime()` do Flask-Babel.

## Checklist de Implementação (Fase 2)

- [ ] Instalar Flask-Babel
- [ ] Criar babel.cfg
- [ ] Adicionar modelo User.locale (CharField, default='pt_BR')
- [ ] Implementar locale selector
- [ ] Extrair strings dos templates com `pybabel extract`
- [ ] Traduzir messages.po para en
- [ ] Compilar traduções
- [ ] Criar UI de seleção de idioma
- [ ] Testar todas as views em ambos idiomas
- [ ] Adicionar testes automatizados i18n
- [ ] Documentar guia de contribuição para novos idiomas

## Roadmap de Idiomas Futuros

**Fase 2:** pt-BR, en  
**Fase 3:** es (espanhol), fr (francês)  
**Fase 4:** ja (japonês) - para comunidade de mangá/light novels

## Referências

- [Flask-Babel Documentation](https://python-babel.github.io/flask-babel/)
- [GNU gettext Manual](https://www.gnu.org/software/gettext/manual/)
- [WCAG 2.1 - Language of Page](https://www.w3.org/WAI/WCAG21/Understanding/language-of-page.html)

---

**Última atualização:** 2025-01-03  
**Responsável:** Larissa Ember  
**Status:** Documentação de preparação completa ✅

