from auth.connect_db import get_conn
from auth.normalisation import norm_email,norm_username

def create_user_pending(username: str, email: str, password_hash: str, token: str) -> None:
    u = norm_username(username)
    e = norm_email(email)

    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (
                    username, email, password_hash,
                    role, is_active, email_verified,
                    email_verification_token
                )
                VALUES (%s, %s, %s, 1, 0, 0, %s)
                """,
                (u, e, password_hash, token),
            )
    finally:
        conn.close()