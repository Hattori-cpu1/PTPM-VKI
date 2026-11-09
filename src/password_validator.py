def validate_password(password: str) -> bool:


    if not isinstance(password, str):
        raise TypeError("Пароль должен быть строкой")

    if ' ' in password:
        raise ValueError("Пароль не должен содержать пробелы")


    if not (8 <= len(password) <= 20):
        return False


    if not any(c.isupper() for c in password):
        return False


    if not any(c.islower() for c in password):
        return False


    if not any(c.isdigit() for c in password):
        return False


    special_chars = "!@#$%^&*"
    if not any(c in special_chars for c in password):
        return False


    return True