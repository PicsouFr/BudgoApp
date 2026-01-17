def norm_username(username: str) -> str:
    return username.strip()


def norm_email(email: str) -> str:
    return str(email).strip().lower()