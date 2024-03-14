from sqlalchemy import func
from app import Book

book_genres = {
    '000': 'General',
    '001': 'Adventure',
    '002': 'Biography',
    '003': 'Mystery',
    '004': 'non-fiction',
    '005': 'Romance',
    '006': '',
    '007': '',
    '008': '',
    '009': '',
    '010': 'Literature',
    '011': 'Young Adult Literature',
    '012': 'Children\'s Literature',
    '013': 'Spanish Literature',
    '014': '',
    '015': '',
    '016': '',
    '017': '',
    '018': '',
    '019': '',
    '020': 'History',
    '021': 'History of the United States',
    '022': 'History of Cinema',
    '023': 'Legal History',
    '024': 'History of Holocaust',
    '025': 'Art History',
    '026': '',
    '027': '',
    '028': '',
    '029': '',
    '030': 'Police Fiction',
    '031': 'Crime Fiction ',
    '032': 'Hardboiled',
    '033': 'Cozy Mystery',
    '034': 'Whodunit',
    '036': 'Noir',
    '037': 'Legal Thriller',
    '038': 'Historical Mystery',
    '039': 'Police Procedural',
    '040': 'fiction',
    '041': 'historical fiction',
    '042': 'Fantasy',
    '043': 'Science fiction',
    '044': 'dystopia',
    '045': '',
    '046': '',
    '047': '',
    '048': '',
    '049': '',
    '050': 'Scientific',
    '051': 'Physics',
    '052': 'Mathematics',
    '053': 'Biology',
    '054': 'Geography',
    '055': 'Astronomy',
    '056': '',
    '057': '',
    '058': '',
    '059': '',
    '060': '',
    '061': '',
    '062': '',
    '063': '',
    '064': '',
    '065': '',
    '066': '',
    '067': '',
    '068': '',
    '069': '',
    '070': '',
    '071': '',
    '072': '',
    '073': '',
    '074': '',
    '075': '',
    '076': '',
    '077': '',
    '078': '',
    '079': '',
    '080': '',
    '081': '',
    '082': '',
    '083': '',
    '084': '',
    '085': '',
    '086': '',
    '087': '',
    '088': '',
    '089': '',
    '090': '',
    '091': '',
    '092': '',
    '093': '',
    '094': '',
    '095': '',
    '096': '',
    '097': '',
    '098': '',
    '099': '',
    '100': '',
    '101': '',
    '102': '',
    '103': '',
    '104': '',
    '105': '',
    '106': '',
    '107': '',
    '108': '',
    '109': '',
    '110': '',
    '111': '',
    '112': '',
    '113': '',
    '114': '',
    '115': '',
    '116': '',
    '117': '',
    '118': '',
    '119': '',
    '120': '',
    '121': '',
    '122': '',
    '123': '',
    '124': '',
    '125': '',
    '126': '',
    '127': '',
    '128': '',
    '129': '',
    '130': '',
    '131': '',
    '132': '',
    '133': '',
    '134': '',
    '135': '',
    '136': '',
    '137': '',
    '138': '',
    '139': '',
    '140': '',
    '141': '',
    '142': '',
    '143': '',
    '144': '',
    '145': '',
    '146': '',
    '147': '',
    '148': '',
    '149': '',
    '150': '',
    '151': '',
    '152': '',
    '153': '',
    '154': '',
    '155': '',
    '156': '',
    '157': '',
    '158': '',
    '159': '',
    '160': '',
    '161': '',
    '162': '',
    '163': '',
    '164': '',
    '165': '',
    '166': '',
    '167': '',
    '168': '',
    '169': '',
    '170': '',
    '171': '',
    '172': '',
    '173': '',
    '174': '',
    '175': '',
    '176': '',
    '177': '',
    '178': '',
    '179': '',
    '180': '',
    '181': '',
    '182': '',
    '183': '',
    '184': '',
    '185': '',
    '186': '',
    '187': '',
    '188': '',
    '189': '',
    '190': '',
    '191': '',
    '192': '',
    '193': '',
    '194': '',
    '195': '',
    '196': '',
    '197': '',
    '198': '',
    '199': '',
    '200': '',
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
