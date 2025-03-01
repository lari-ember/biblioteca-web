# app/utils/security.py
import re

def validate_password_complexity(password):
    """Valida complexidade da senha (mínimo 8 caracteres, 1 maiúscula, 1 número)"""
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    return True