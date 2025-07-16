def sanitize_string(value, case=None):
    """
    Limpa e padroniza uma string.
    case: 'title', 'capitalize', 'lower', None
    """
    if not isinstance(value, str):
        return value
    value = value.strip()
    if case == 'title':
        return value.title()
    elif case == 'capitalize':
        return value.capitalize()
    elif case == 'lower':
        return value.lower()
    return value

