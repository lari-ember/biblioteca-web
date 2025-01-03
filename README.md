📚 Biblioteca Web

Um sistema de gerenciamento de bibliotecas desenvolvido com Flask e SQLAlchemy, permitindo que usuários façam cadastro, gerenciem coleções de livros, emprestem e pesquisem informações sobre livros utilizando a API da Open Library. Este projeto também inclui integração com Docker para facilitar o deploy e o desenvolvimento.
🖥️ Demonstração

    URL da aplicação local: http://localhost
    Requisitos para acesso: Navegador web compatível (Chrome, Firefox).

🚀 Funcionalidades

    Gerenciamento de Usuários:
        Cadastro e login de usuários.
        Gerenciamento de perfis.

    Gerenciamento de Livros:
        Registro de novos livros com informações completas (autor, título, ano, gênero, formato, etc.).
        Visualização da coleção de livros pessoais.
        Pesquisas detalhadas com filtros customizados.
        Empréstimos de livros entre usuários.

    APIs e Integrações:
        Busca e registro de informações sobre livros utilizando a Open Library API.
        Verificação de capas de livros por ISBN.

    Administração:
        Gerenciamento global de livros (edição e exclusão por administradores).
        Visualização de dados sobre o sistema.

    Estilo e Design:
        Estilos personalizados com suporte para CSS avançado.
        Autocompletar para busca por títulos.

🛠️ Tecnologias
Backend:

    Python (3.10+)
    Flask e Flask-Login
    SQLAlchemy
    psycopg2 (para integração com PostgreSQL)

Frontend:

    HTML5
    CSS3 (com arquivos como product.css, estilos.css, pestilio.css e more.css)
    JavaScript:
        Integração com APIs externas.
        Scripts para autocomplete de títulos.

DevOps:

    Docker:
        Configurado para rodar o Flask, PostgreSQL e Nginx.
        Imagens separadas para banco de dados e backend.
    Nginx:
        Proxy reverso configurado para balancear a aplicação.
    PostgreSQL:
        Utilizado para armazenar informações de usuários e livros.

📂 Estrutura do Projeto

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

⚙️ Instalação e Uso
Pré-requisitos

    Docker (recomendado)
    Python (para rodar localmente)
    PostgreSQL (banco de dados)

Configuração Local com Docker

    Clone o repositório:

git clone https://github.com/lari-ember/biblioteca-web.git
cd biblioteca-web

Inicie os containers:

docker-compose up --build

Acesse a aplicação:

    Abra o navegador e acesse: http://localhost

Para encerrar os containers:

    docker-compose down

🧪 Testes

O projeto inclui testes para validar a funcionalidade de rotas e modelos.

    Executar testes:

    python -m unittest discover tests

🔧 Solução de Problemas

    Erro 502 no Nginx:
        Verifique se os containers estão em execução.
        Reinicie os serviços:

    docker-compose down && docker-compose up --build

Banco de dados com dados persistentes indesejados:

    Limpe os volumes do Docker:

        docker volume rm $(docker volume ls -q)

    Problemas de rede em API externa (Open Library):
        Tente verificar sua conexão e o status da API aqui.

🌟 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou pull requests.
📜 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
👩‍💻 Autor

Desenvolvido por Larissa Ember.
Siga no GitHub para mais projetos.
