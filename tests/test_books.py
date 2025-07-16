def test_register_new_book_form(test_client):
    # Simula login (ajuste conforme seu sistema de autenticação)
    with test_client.session_transaction() as sess:
        sess['user_id'] = 1  # Supondo que o usuário 1 existe no banco de teste

    # Dados do livro para cadastro
    data = {
        'title': 'Automated Test Book',
        'author': 'Test Author',
        'genre': 'Fiction',
        'year': 2024,
        'pages': 123,
        'publisher': 'Test Publisher',
        'format': 'ebook'
    }
    response = test_client.post('/register_new_book', data=data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Automated Test Book' in response.data

