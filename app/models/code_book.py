from sqlalchemy import func
from app import Book

book_genres = {
    '000': 'General',
    '001': 'Essay',
    '002': 'Biography',
    '003': 'Mystery',
    '004': 'Non-fiction',
    '005': 'Romance',
    '006': 'Sapphic',
    '007': 'Fact List',
    '008': '',
    '009': '',
    '100': 'Literature',
    '110': 'United States Literature',
    '111': 'United States Romance',
    '112': 'United States Theatre',
    '113': 'United States Young Adult Literature',
    '114': 'United States Children\'s Literature',
    '120': 'English Literature',
    '121': 'English Romance',
    '122': 'English Theatre',
    '130': 'Spanish Literature',
    '140': 'Brazilian Literature',
    '150': 'Portuguese Literature',
    '151': 'Portuguese Romance',
    '152': 'Portuguese Theatre',
    '160': 'Middle East Literature',
    '161': 'Middle East Romance',
    '162': 'Middle East Theatre',
    '163': 'Middle East Poetry',
    '170': '',
    '180': '',
    '190': '',
    '200': 'History',
    '210': 'History of the United States',
    '220': 'History of the Cinema',
    '230': 'History of europe',
    '231': 'History of Holocaust',
    '240': 'History of art',
    '260': '',
    '270': '',
    '280': '',
    '300': 'Fiction',
    '310': 'Fantasy',
    '320': 'Science fiction',
    '321': 'Geographic Science fiction',
    '322': 'Time Travel',
    '330': 'Police Fiction',
    '331': 'Crime Fiction ',
    '332': 'Hardboiled',
    '333': 'Cozy Mystery',
    '334': 'Whodunit',
    '335': 'Noir',
    '336': 'Legal Thriller',
    '337': 'Historical Mystery',
    '338': 'Police Procedural',
    '339': 'Thriller',
    '340': 'Historical Fiction',
    '350': 'Dystopia',
    '360': 'Adventure',
    '370': '',
    '380': '',
    '390': '',
    '400': '',
    '410': '',
    '420': '',
    '430': '',
    '440': '',
    '450': '',
    '460': '',
    '470': '',
    '480': '',
    '490': '',
    '500': 'Scientific',
    '510': 'Physics',
    '520': 'Mathematics',
    '530': 'Biology',
    '540': 'Geography',
    '550': 'Astronomy',
    '560': 'Philosophy',
    '570': 'social Sciences',
    '571': 'Sociology',
    '572': 'Political Economy',
    '573': 'Economy',
    '574': 'Anthropology',
    '580': 'psychology',
    '590': '',
    '600': 'Law',
    '610': 'Legal History',
    '620': 'Theory of Law',
    '630': 'Philosophy of Law',
    '640': 'Political Science',
    '650': '',
    '660': '',
    '670': 'Sociology of Law',
    '680': '',
    '690': '',
    '700': 'Graphic',
    '710': 'Manga',
    '711': 'Manga Yuri',
    '720': 'Novel',
    '721': 'Graphic Novel Sapphic',
    '730': '',
    '740': '',
    '750': '',
    '760': '',
    '770': '',
    '780': '',
    '790': '',
    '800': '',
    '810': '',
    '820': '',
    '830': '',
    '840': '',
    '850': '',
    '860': '',
    '870': '',
    '880': '',
    '890': '',
    '900': '',
    '910': '',
    '920': '',
    '930': '',
    '940': '',
    '950': '',
    '960': '',
    '970': '',
    '980': '',
    '990': '',
}


def generate_book_code(genre, author_fullname, title):
    # Obtenha o último sobrenome do autor
    author_lastname = author_fullname.split()[-1]

    # Obtenha a primeira letra do último sobrenome do autor
    author_lastname_initial = author_lastname[0]

    title_initial = title[0]
    
    genre = genre.title()

    # Verifique se o gênero está presente no dicionário de gêneros
    if genre.title() in book_genres.values():
        # Encontre a chave correspondente ao gênero no dicionário de gêneros
        genre_code = next((key for key, value in book_genres.items() if value == genre), None)
        if genre_code:
            base_code = f'{author_lastname_initial.upper()}{genre_code}{title_initial.lower()}'
            print(base_code)

            last_code = Book.query.filter(Book.code.like(f'{base_code}%')).order_by(Book.code.desc()).first()

            if last_code:
                # Obtenha o sufixo do último código usado
                last_suffix = last_code.code[len(base_code) + 1:]
                # Verifique se o sufixo é um número
                if last_suffix.isdigit():
                    # Incremente o sufixo
                    new_suffix = f'.{str(int(last_suffix) + 1).zfill(3)}'
                    # Gere o novo código com o sufixo
                    new_code = f'{base_code}{new_suffix}'
                else:
                    # O último sufixo não é um número, então adicione ".001" como sufixo
                    new_code = f'{base_code}.001'
            else:
                # Não existem códigos com base_code, então use o código base
                new_code = base_code

            return new_code
        else:
            # Não encontrou o gênero no dicionário de gêneros
            return None
    else:
        # O gênero não está presente no dicionário de gêneros
        return None

