import csv
from . import db, Book


def add_books_from_csv(file_path):
    with open(file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            book = Book(
                code=row['codigo'],
                title=row['titulo'],
                author=row['autore'],
                publisher=row['editora'],
                year=row['ano'],
                pages=row['paginas'],
                read=row['lido'],
                genre=row['genero'],
                format=row['formato']
            )
            db.session.add(book)
            db.session.commit()

# Caminho para o arquivo CSV de exemplo
csv_file_path = 'C:/Users/bolsista.SFDA-DOACAO-BOL/Documents/GitHub/Biblioteca/acervo.csv'

# Chame a função para adicionar os livros do CSV
add_books_from_csv(csv_file_path)
