from auth.connect_db import get_conn
from auth.normalisation import norm_email, norm_username

def username_exists(username: str) -> bool:
    u = norm_username(username)
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM users WHERE username = %s LIMIT 1",
                (u,)
            )
            return cur.fetchone() is not None
    finally:
        conn.close()


def email_exists(email: str) -> bool:
    m = norm_email(email)
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT 1 FROM users WHERE email = %s LIMIT 1",
                (m,)
            )
            return cur.fetchone() is not None
    finally:
        conn.close()
