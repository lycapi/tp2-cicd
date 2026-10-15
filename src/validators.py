import re


def is_valid_email(email):
    if not email or not isinstance(email, str):
        return False
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return bool(re.match(pattern, email))


def is_valid_password(password):
    if not password or not isinstance(password, str):
        return {
            "valid": False,
            "errors": ["Mot de passe vide ou invalide"]
        }

    errors = []
    if len(password) < 8:
        errors.append("Au moins 8 caractères requis")
    if not re.search(r"[A-Z]", password):
        errors.append("Au moins 1 majuscule requise")
    if not re.search(r"[a-z]", password):
        errors.append("Au moins 1 minuscule requise")
    if not re.search(r"[0-9]", password):
        errors.append("Au moins 1 chiffre requis")
    if not re.search(r"[!@#$%^&*]", password):
        errors.append("Au moins 1 caractère spécial requis")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }


def is_valid_age(age):
    if age is None or isinstance(age, bool):
        return False
    if not isinstance(age, int):
        return False
    return 0 <= age <= 150
