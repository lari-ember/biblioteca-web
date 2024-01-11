from sqlalchemy import func
from app import Book

book_genres = {
    '000': 'General',
    '001': 'Adventure',
    '002': 'Biography',
    '003': 'Mystery',
    '004': 'Children\'s Literature',
    '005': 'Romance',
    '006': 'Fiction',
    '007': 'Crime Fiction',
    '008': 'Scientific',
    '009': 'Fantasy',
    '010': 'Holocaust History',
    '011': 'Dystopia',
    '012': 'Self-Help',
    '013': 'Young Adult Literature',
    '014': 'Poetry',
    '015': 'Theatre',
    '016': 'Essay',
    '017': 'Letter',
    '018': 'Satire',
    '019': 'Psychology',
    '020': 'Law',
    '021': 'Sociology',
    '022': 'Sociology of Law',
    '023': 'Political Science',
    '024': 'Sociology of Law',
    '025': 'Philosophy of Law',
    '026': 'Legal Theory',
    '027': 'Criticism',
    '028': 'Political Economy',
    '029': 'Science Fiction',
    '030': 'Legal History',
    '031': 'Short Story',
    '032': 'History',
    '033': 'Sapphic',
    '034': 'Fact List',
    '036': 'History',
    '037': 'Historical Fiction',
    '038': 'Medicine',
    '039': 'Nursing',
    '040': 'Dentistry',
    '041': 'Civil Engineering',
    '042': 'Mechanical Engineering',
    '043': 'Electrical Engineering',
    '044': 'Software Engineering',
    '045': 'Chemical Engineering',
    '046': 'Biomedical Engineering',
    '047': 'Environmental Engineering',
    '048': 'Food Engineering',
    '049': 'Production Engineering',
    '050': 'Chemistry',
    '051': 'Physics',
    '052': 'Mathematics',
    '053': 'Biology',
    '054': 'Geography',
    '055': 'Astronomy',
    '056': 'Sociology of Education',
    '057': 'Pedagogy',
    '058': 'Physical Education',
    '059': 'Educational Psychology',
    '060': 'Technology',
    '061': 'Arts',
    '062': 'Design',
    '063': 'Fashion',
    '064': 'Photography',
    '065': 'Music',
    '066': 'Dance',
    '067': 'Cinema',
    '068': 'Art History',
    '069': 'Architecture',
    '070': 'Computer Science',
    '071': 'Artificial Intelligence',
    '072': 'Computer Networks',
    '073': 'Information Security',
    '074': 'Information Systems',
    '075': 'Database',
    '076': 'Programming',
    '077': 'Software Engineering',
    '078': 'Web Design',
    '079': 'User Interface',
    '080': 'Marketing',
    '081': 'Management',
    '082': 'Finance',
    '083': 'Human Resources',
    '084': 'Entrepreneurship',
    '085': 'Project Management',
    '086': 'International Business',
    '087': 'Economics',
    '088': 'Accounting',
    '089': 'Statistics',
    '090': 'Agriculture',
    '091': 'Environment',
    '092': 'Zoology',
    '093': 'Botany',
    '094': 'Ecology',
    '095': 'Geology',
    '096': 'Meteorology',
    '097': 'Paleontology',
    '098': 'Anthropology',
    '099': 'Archaeology',
    '100': 'Linguistics',
    '101': 'Sociology of Gender',
    '102': 'Political Philosophy',
    '103': 'World History',
    '104': 'Mythology',
    '105': 'Cultural Studies',
    '106': 'Literary Criticism',
    '107': 'Environmental Science',
    '108': 'Energy',
    '109': 'Public Health',
    '110': 'Sociology of Work',
    '111': 'Cognitive Psychology',
    '112': 'Business Strategy',
    '113': 'International Relations',
    '114': 'Social Media',
    '115': 'Data Science',
    '116': 'Cybersecurity',
    '117': 'Artificial Neural Networks',
    '118': 'Robotics',
    '119': 'Virtual Reality',
    '120': 'Natural Language Processing',
    '121': 'Game Development',
    '122': 'Graphic Design',
    '123': 'Interior Design',
    '124': 'Film Production',
    '125': 'Art Therapy',
    '126': 'Music Therapy',
    '127': 'Philosophy of Mind',
    '128': 'Ethics',
    '129': 'Social Theory',
    '130': 'Urban Planning',
    '131': 'Behavioral Economics',
    '132': 'Organizational Behavior',
    '133': 'Microbiology',
    '134': 'Genetics',
    '135': 'Evolutionary Biology',
    '136': 'Earth Science',
    '137': 'Oceanography',
    '138': 'Quantum Physics',
    '139': 'Astrophysics',
    '140': 'Sociology of Religion',
    '141': 'Education Policy',
    '142': 'Sign Language Linguistics',
    '143': 'Developmental Psychology',
    '144': 'Digital Marketing',
    '145': 'Supply Chain Management',
    '146': 'Corporate Finance',
    '147': 'Risk Management',
    '148': 'Operations Management',
    '149': 'Econometrics',
    '150': 'Animal Science',
    '151': 'Conservation Biology',
    '152': 'Horticulture',
    '153': 'Marine Biology',
    '154': 'Paleobotany',
    '155': 'Sociology of Health',
    '156': 'Gender Studies',
    '157': 'Human Rights',
    '158': 'Peace Studies',
    '159': 'Art History',
    '160': 'Comparative Literature',
    '161': 'Archaeoastronomy',
    '162': 'Geopolitics',
    '163': 'Human Geography',
    '164': 'Industrial Design',
    '165': 'User Experience Design',
    '166': 'Multimedia Design',
    '167': 'Screenwriting',
    '168': 'Animation',
    '169': 'Art Education',
    '170': 'Dance Therapy',
    '171': 'Philosophy of Science',
    '172': 'Metaphysics',
    '173': 'Social Justice',
    '174': 'Sociology of Deviance',
    '175': 'Media Studies',
    '176': 'Cryptography',
    '177': 'Machine Learning',
    '178': 'Augmented Reality',
    '179': 'Data Visualization',
    '180': 'Web Development',
    '181': 'Mobile App Development',
    '182': 'Product Design',
    '183': 'Film Studies',
    '184': 'Musicology',
    '185': 'Music Composition',
    '186': 'Music Production',
    '187': 'Drama Therapy',
    '188': 'Artificial General Intelligence',
    '189': 'Digital Humanities',
    '190': 'Cultural Anthropology',
    '191': 'Sociolinguistics',
    '192': 'Urban Sociology',
    '193': 'Behavioral Psychology',
    '194': 'Corporate Law',
    '195': 'Human Resource Management',
    '196': 'Social Media Marketing',
    '197': 'Statistical Analysis',
    '198': 'Biochemistry',
    '199': 'Neuroscience',
    '200': 'History of the United States',
    '201': 'Philosophy',
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
