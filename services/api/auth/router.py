import secrets
from passlib.context import CryptContext
from fastapi import APIRouter, Query, HTTPException, status
from auth.connect_db import get_conn
from auth.verif_user_exist import username_exists, email_exists
from auth.register_in_and_out import RegisterIn, RegisterOut
from auth.normalisation import norm_email,norm_username
from auth.create_user_pending import create_user_pending
from auth.send_email_activation import send_activation_email


router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

@router.get("/ping")
def auth_ping():
    return {"auth": "ok"}

@router.get("/db-test")
def db_test():
    try:
        conn = get_conn()
        with conn.cursor() as cur:
            cur.execute("SELECT 1 AS ok")
            row = cur.fetchone()
        conn.close()
        return {"db": "ok", "result": row}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/check")
def check_availability(
    username: str | None = Query(None, min_length=3, max_length=32),
    email: str | None = Query(None),
):
    username = username.strip() if username else None
    email = email.strip().lower() if email else None

    if not username and not email:
        raise HTTPException(status_code=400, detail="pseudo ou email requis")
    
    return {
        "username_available": False if username and username_exists(username) else True,
        "email_available": False if email and email_exists(email) else True,
    }

@router.post("/register", response_model=RegisterOut, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterIn):
    username = norm_username(payload.username)
    email = norm_email(payload.email)

    errors = {}
    if username_exists(username):
        errors["username"] = "Pseudo déjà utilisé"
    if email_exists(email):
        errors["email"] = "Email déjà utilisé"
    if errors:
        raise HTTPException(status_code=409, detail={"errors": errors})
    
    pw = payload.password
    print("PW DEBUG:", "chars=", len(pw), "bytes=", len(pw.encode("utf-8")), "starts=", repr(pw[:30]))
    password_hash = pwd_context.hash(pw)

    token = secrets.token_urlsafe(32)
    create_user_pending(
        username=username,
        email=email,
        password_hash=password_hash,
        token=token
    )

    send_activation_email(email, username, token)

    return {"ok": True}

@router.get("/activate")
def activate(token: str = Query(..., min_length=10)):
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE users
                SET is_active=1,
                    email_verified=1,
                    email_verification_token=NULL
                WHERE email_verification_token=%s
                """,
                (token,),
            )
            if cur.rowcount != 1:
                raise HTTPException(status_code=400, detail="Invalid token")
    finally:
        conn.close()

    return {"ok": True}
