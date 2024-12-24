def get_author_info(author_id):
    url = f"https://openlibrary.org{author_id}.json" #url = f"https://openlibrary.org/search.json?q={author_id}"
    response = requests.get(url)
    if response.status_code == 200:
        author_data = response.json()
        author_name = author_data['name']
        return author_name
    else:
        print(f"Erro ao obter informações do livro. Código de status: {response.status_code}")
        return None

#13195984
def get_book_year(isbn):
    book_info = get_book_info(isbn)
    url = f"https://openlibrary.org/search.json?q={book_info}"
    response = requests.get(url)
    book_data = response.json()
    if response.status_code == 200:
        return book_data['docs'][0]['first_publish_year']


def gret_book_cover_urls(isbn):
    #book_isbn = get_book_isbn(isbn)
    book_info = get_book_info(isbn)
    urls = [
    "https://cdn2.stablediffusionapi.com/generations/0-2c9cacfd-79a7-4463-9556-728a69da79de.png",
    "https://cdn2.stablediffusionapi.com/generations/0-b727fd5e-ac29-4195-a7e0-f5a355b932f7.png",
    "https://cdn2.stablediffusionapi.com/generations/0-9b3afd4e-e8de-49d4-b131-38353c5bc479.png",
    "https://marketplace.canva.com/EAF4ezr7wzw/1/0/1003w/canva-capa-de-livro-e-caderno-de-reda%C3%A7%C3%A3o-escolar-papel-com-rabiscos-vermelho-e-preto-N3f0RoEPy9U.jpg"
]
    print(book_info)
    if book_info and "covers" in book_info:
        cover_id = book_info["covers"][0]  # Pode ser "small", "medium" ou "large"
        return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    else:
        print(isbn)
        amazonURL = f'https://amazon.com.br/dp/{isbn}'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        }
        try:
            response = requests.get(amazonURL, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                image_tag = soup.find(id='landingImage')
                if image_tag:
                    return image_tag['src']
                else:
                    print("Image element not found on the page.")
                    return urls[0]
            else:
                print(f"Failed to fetch the page. Status code: {response.status_code}")
                return urls[1]
        except requests.RequestException as e:
            print(f"Error fetching the page: {e}")
            return urls[2]
        else:
            return urls[3]

# Exemplo de uso

#isbn = '9798683678777'  # Replace with the desired ISBN

import requests
from bs4 import BeautifulSoup


def search_book_by_title(title):
    """
    Busca um livro pelo título e retorna o primeiro ISBN encontrado.
    """
    url = f"https://openlibrary.org/search.json?q={title}"
    response = requests.get(url)
    if response.status_code == 200:
        book_data = response.json()
        try:
            return book_data['docs'][0]['isbn'][1]  # Primeiro ISBN disponível
        except (IndexError, KeyError):
            return 'Na'  # Não encontrou ISBN
    else:
        print(f"Erro ao buscar o livro. Código de status: {response.status_code}")
        return 'Na'


def get_book_info(isbn):
    """
    Retorna informações detalhadas do livro a partir do ISBN.
    """
    url = f"https://openlibrary.org/search.json?q={isbn}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erro ao obter informações do livro. Código de status: {response.status_code}")
        return None


def get_author_name(author_key):
    """
    Obtém o nome do autor a partir de sua chave.
    """
    url = f"https://openlibrary.org{author_key}.json"
    response = requests.get(url)
    if response.status_code == 200:
        author_data = response.json()
        return author_data.get('name', 'Autor desconhecido')
    else:
        print(f"Erro ao buscar informações do autor. Código de status: {response.status_code}")
        return None


def get_book_cover_url(isbn):
    """
    Obtém a URL da capa do livro usando o ISBN.
    Se não for encontrada na Open Library, tenta buscar na Amazon."
    """
    book_info = get_book_info(isbn)
    fallback_urls = [
        "https://i.ibb.co/mT21xJH/Newton-s-Principia-title-page.png",
        "https://i.ibb.co/VjQSZt2/capa1.webp",
        "https://i.ibb.co/D4gR1NB/capa2.webp"
    ]

    # Verifica se os dados do livro possuem o campo 'cover_i'
    try:
        cover_id = book_info['docs'][0]['cover_i']  # Obtém o cover_i do primeiro resultado em 'docs'
        return f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
    except (KeyError, IndexError):
        # Se não encontrar o cover_i
        #Caso contrário, tenta buscar na Amazon
        amazon_url = f'https://amazon.com.br/dp/{book_info.get("isbn", [""])[0]}'
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
        }
        try:
            response = requests.get(amazon_url, headers=headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                image_tag = soup.find(id='landingImage')
                if image_tag:
                    return image_tag['src']
        except requests.RequestException as e:
            print(f"Erro ao buscar capa na Amazon: {e}")
            return fallback_urls[1]
        else:
            # Retorna uma URL de fallback se todas as tentativas falharem
            return fallback_urls[2]


def get_book_year(isbn):
    """
    Obtém o ano da primeira publicação do livro usando o ISBN.
    """
    book_info = get_book_info(isbn)
    if book_info:
        return book_info.get('publish_date', 'Ano desconhecido')
    else:
        return 2024