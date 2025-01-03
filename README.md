---

# 📚 Biblioteca Web

Um sistema de gerenciamento de bibliotecas desenvolvido com **Flask** e **SQLAlchemy**, permitindo que usuários façam cadastro, gerenciem coleções de livros, emprestem e pesquisem informações sobre livros utilizando a [API da Open Library](https://openlibrary.org/developers/api). Este projeto também inclui integração com **Docker** para facilitar o deploy e o desenvolvimento.

---

## 🖥️ Demonstração

- **URL da aplicação local**: [http://localhost](http://localhost)  
- **Requisitos para acesso**: Navegador web compatível (Chrome, Firefox).

---

## 🚀 Funcionalidades

### Gerenciamento de Usuários:
- Cadastro e login de usuários.
- Gerenciamento de perfis.

### Gerenciamento de Livros:
- Registro de novos livros com informações completas (autor, título, ano, gênero, formato, etc.).
- Visualização da coleção de livros pessoais.
- Pesquisas detalhadas com filtros customizados.
- Empréstimos de livros entre usuários.

### APIs e Integrações:
- Busca e registro de informações sobre livros utilizando a [Open Library API](https://openlibrary.org/developers/api).
- Verificação de capas de livros por ISBN.

### Administração:
- Gerenciamento global de livros (edição e exclusão por administradores).
- Visualização de dados sobre o sistema.

### Estilo e Design:
- Estilos personalizados com suporte para CSS avançado.
- Autocompletar para busca por títulos.

---

## 🛠️ Tecnologias

### Backend:
- **[Python](https://www.python.org/)** (3.10+)
- **[Flask](https://flask.palletsprojects.com/)** e **[Flask-Login](https://flask-login.readthedocs.io/)**
- **[SQLAlchemy](https://docs.sqlalchemy.org/)**
- **[psycopg2](https://www.psycopg.org/docs/)** (para integração com PostgreSQL)

### Frontend:
- **HTML5** e **[Jinja2](https://jinja.palletsprojects.com/en/3.0.x/)** (templates dinâmicos)
- **CSS3** (com arquivos como `product.css`, `estilos.css`, `pestilio.css` e `more.css`)
- **JavaScript**:
  - Integração com APIs externas.
  - Scripts para autocomplete de títulos.

### DevOps:
- **[Docker](https://docs.docker.com/)**:
  - Configurado para rodar o Flask, PostgreSQL e Nginx.
  - Imagens separadas para banco de dados e backend.
- **[Nginx](https://nginx.org/)**:
  - Proxy reverso configurado para balancear a aplicação.
- **[PostgreSQL](https://www.postgresql.org/)**:
  - Utilizado para armazenar informações de usuários e livros.

---

## 📂 Estrutura do Projeto

```plaintext
biblioteca-web/
├── app/
│   ├── controllers/
│   │   ├── auth.py  # Gerenciamento de usuários
│   │   ├── books.py # Gerenciamento de livros
│   │   ├── default.py # Rotas padrão (index, home, etc.)
│   ├── models/
│   │   ├── book.py # Definição do modelo "Book"
│   │   ├── user.py # Definição do modelo "User"
│   ├── templates/
│   │   ├── register_new_book.html # Página de registro de livros
│   │   ├── login.html # Página de login
│   │   ├── your_collection.html # Página da coleção do usuário
│   └── static/
│       ├── css/ # Arquivos de estilo
│       ├── js/  # Scripts
├── tests/
│   └── test_app.py # Testes unitários e de integração
├── Dockerfile
├── docker-compose.yml
├── README.md
```

---

## ⚙️ Instalação e Uso

### Pré-requisitos
- **[Docker](https://docs.docker.com/get-docker/)** (recomendado)
- **[Python](https://www.python.org/)** (para rodar localmente)
- **[PostgreSQL](https://www.postgresql.org/)** (banco de dados)

### Configuração Local com Docker

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/lari-ember/biblioteca-web.git
   cd biblioteca-web
   ```

2. **Inicie os containers**:
   ```bash
   docker-compose up --build
   ```

3. **Acesse a aplicação**:
   - Abra o navegador e acesse: [http://localhost](http://localhost)

4. **Para encerrar os containers**:
   ```bash
   docker-compose down
   ```

---

## 🧪 Testes

O projeto inclui testes para validar a funcionalidade de rotas e modelos.

- **Executar testes**:
  ```bash
  python -m unittest discover tests
  ```

---

## 🔧 Solução de Problemas

- **Erro 502 no Nginx**:
  - Verifique se os containers estão em execução.
  - Reinicie os serviços:
    ```bash
    docker-compose down && docker-compose up --build
    ```

- **Banco de dados com dados persistentes indesejados**:
  - Limpe os volumes do Docker:
    ```bash
    docker volume rm $(docker volume ls -q)
    ```

- **Problemas de rede em API externa (Open Library)**:
  - Verifique sua conexão e o status da API [aqui](https://status.openlibrary.org/).

---

## 🌟 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir [issues](https://github.com/lari-ember/biblioteca-web/issues) ou enviar [pull requests](https://github.com/lari-ember/biblioteca-web/pulls).

---

## 📜 Licença

Este projeto está licenciado sob a [licença MIT](LICENSE).

---

## 👩‍💻 Autor

Desenvolvido por **[Larissa Ember](https://github.com/lari-ember)**.  
[Siga no GitHub](https://github.com/lari-ember) para mais projetos.

---
