# BUDGOAPPV2/api/budgo/app/routers/auth.py
# CREATED BY José

import os
import secrets
import pymysql
from pymysql.cursors import DictCursor

from fastapi import APIRouter, Query, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from passlib.context import CryptContext

import smtplib
from email.mime.text import MIMEText
from typing import Optional



router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------- Models ----------
class AvailabilityOut(BaseModel):
    username_available: bool
    email_available: bool


class RegisterIn(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class RegisterOut(BaseModel):
    ok: bool


# ---------- MySQL config ----------
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = int(os.getenv("MYSQL_PORT"))
MYSQL_DB = os.getenv("MYSQL_DB")
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
# ---------- BREVO config ----------
BREVO_SMTP_HOST = os.environ["BREVO_SMTP_HOST"]
BREVO_SMTP_PORT = int(os.environ["BREVO_SMTP_PORT"])
BREVO_SMTP_USER = os.environ["BREVO_SMTP_USER"]
BREVO_SMTP_PASS = os.environ["BREVO_SMTP_PASS"]
BREVO_SENDER_EMAIL = os.environ["BREVO_SENDER_EMAIL"]
BREVO_SENDER_NAME = os.environ["BREVO_SENDER_NAME"]
PUBLIC_SITE_URL = os.environ["PUBLIC_SITE_URL"]



def get_conn():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset="utf8mb4",
        autocommit=True,
        cursorclass=DictCursor,
    )


# ---------- Normalization ----------
def norm_username(username: str) -> str:
    return username.strip()


def norm_email(email: str) -> str:
    return str(email).strip().lower()


# ---------- DB helpers ----------
def username_exists(username: str) -> bool:
    u = norm_username(username)
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE username=%s LIMIT 1", (u,))
            return cur.fetchone() is not None
    finally:
        conn.close()


def email_exists(email: str) -> bool:
    e = norm_email(email)
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1 FROM users WHERE email=%s LIMIT 1", (e,))
            return cur.fetchone() is not None
    finally:
        conn.close()


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

def send_activation_email(to_email: str, username: str, token: str) -> None:
    if not BREVO_SMTP_USER or not BREVO_SMTP_PASS:
        raise HTTPException(status_code=500, detail="SMTP not configured")

    link = f"{PUBLIC_SITE_URL}/activate.php?token={token}"

    html = f"""\
    <!doctype html>
    <html lang="fr">
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>Activation BudgoApp</title>
    </head>
    <body style="margin:0;padding:0;background:#05070c;">
    <!-- Background -->
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#05070c;padding:40px 12px;">
        <tr>
        <td align="center">

            <!-- Outer glow card -->
            <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="
            width:600px;max-width:600px;
            border-radius:18px;
            background: linear-gradient(135deg, rgba(26, 160, 170, .18), rgba(116, 92, 255, .14)) , #0b1020;
            border:1px solid rgba(140, 170, 255, .18);
            box-shadow: 0 24px 70px rgba(0,0,0,.65);
            overflow:hidden;
            ">
            <tr>
                <td style="padding:26px 26px 0 26px;">
                <!-- top bar -->
                <div style="
                    height:10px;border-radius:999px;
                    background: linear-gradient(90deg, rgba(27, 190, 200, .35), rgba(110, 110, 255, .35));
                    opacity:.9;
                "></div>
                </td>
            </tr>

            <tr>
                <td style="padding:22px 26px 10px 26px;" align="center">
                <img src="https://budgoapp.com/public/img/logo_site.png"
                    width="120" alt="BudgoApp"
                    style="display:block;border:0;outline:none;text-decoration:none;height:auto;">
                </td>
            </tr>

            <tr>
                <td style="padding:8px 34px 0 34px;">
                <div style="
                    font-family: Arial, sans-serif;
                    font-size:28px;
                    line-height:1.15;
                    font-weight:800;
                    color:#ffffff;
                    letter-spacing:-.2px;
                    text-align:left;
                ">
                    Bienvenue sur BudgoApp, {username} 👋
                </div>

                <div style="
                    margin-top:10px;
                    font-family: Arial, sans-serif;
                    font-size:15px;
                    line-height:1.65;
                    color:rgba(230,235,255,.82);
                    text-align:left;
                ">
                    Merci de t’être inscrit. Pour activer ton compte, clique sur le bouton ci-dessous.
                </div>
                </td>
            </tr>

            <tr>
                <td align="center" style="padding:22px 34px 10px 34px;">
                <!-- Button -->
                <a href="{link}" style="
                    display:inline-block;
                    padding:14px 26px;
                    border-radius:12px;
                    text-decoration:none;
                    font-family: Arial, sans-serif;
                    font-size:15px;
                    font-weight:800;
                    color:#ffffff;
                    background: linear-gradient(90deg, rgba(27,190,200,.55), rgba(110,110,255,.55));
                    border:1px solid rgba(160,190,255,.35);
                    box-shadow: 0 14px 40px rgba(0,0,0,.55);
                ">
                    ✅ Activer mon compte
                </a>
                </td>
            </tr>

            <tr>
                <td style="padding:12px 34px 0 34px;">
                <div style="
                    font-family: Arial, sans-serif;
                    font-size:13px;
                    line-height:1.6;
                    color:rgba(185,195,255,.75);
                    text-align:left;
                ">
                    Si le bouton ne marche pas, copie-colle ce lien dans ton navigateur :
                </div>
                <div style="
                    margin-top:8px;
                    padding:12px 14px;
                    border-radius:12px;
                    background: rgba(255,255,255,.04);
                    border:1px solid rgba(140,170,255,.14);
                    font-family: Arial, sans-serif;
                    font-size:12px;
                    line-height:1.45;
                    color:rgba(230,235,255,.88);
                    word-break:break-all;
                    text-align:left;
                ">
                    {link}
                </div>
                </td>
            </tr>

            <tr>
                <td style="padding:18px 34px 26px 34px;">
                <div style="
                    font-family: Arial, sans-serif;
                    font-size:12px;
                    line-height:1.6;
                    color:rgba(160,170,230,.7);
                    text-align:left;
                ">
                    Si tu n’as pas créé ce compte, ignore ce message.
                </div>

                <div style="
                    margin-top:16px;
                    font-family: Arial, sans-serif;
                    font-size:12px;
                    color:rgba(160,170,230,.55);
                    text-align:center;
                ">
                    © 2025 BudgoApp — Tous droits réservés
                </div>
                </td>
            </tr>
            </table>

        </td>
        </tr>
    </table>
    </body>
    </html>
    """

    msg = MIMEText(html, "html", "utf-8")
    msg["Subject"] = "Activation de votre compte BudgoApp"
    msg["From"] = f"{BREVO_SENDER_NAME} <{BREVO_SENDER_EMAIL}>"
    msg["To"] = to_email

    try:
        with smtplib.SMTP(BREVO_SMTP_HOST, BREVO_SMTP_PORT, timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(BREVO_SMTP_USER, BREVO_SMTP_PASS)
            server.sendmail(BREVO_SENDER_EMAIL, [to_email], msg.as_string())
    except smtplib.SMTPException:
        raise HTTPException(status_code=502, detail="Brevo SMTP send failed")

@router.get("/availability", response_model=AvailabilityOut)
def availability(
    username: Optional[str] = Query(None, min_length=3, max_length=32),
    email: Optional[EmailStr] = Query(None),
):
    if username is None and email is None:
        raise HTTPException(status_code=422, detail="username or email required")

    u = norm_username(username) if username else None
    e = norm_email(email) if email else None

    return {
        "username_available": True if u is None else (not username_exists(u)),
        "email_available": True if e is None else (not email_exists(e)),
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

    password_hash = pwd_context.hash(payload.password)

    token = secrets.token_urlsafe(32)
    create_user_pending(username=username, email=email, password_hash=password_hash, token=token)

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
