from email.mime.text import MIMEText
import os
import smtplib
from fastapi import HTTPException

BREVO_SMTP_HOST = os.getenv("MAIL_HOST")
BREVO_SMTP_PORT = int(os.getenv("MAIL_PORT"))
BREVO_SMTP_USER = os.getenv("MAIL_USER")
BREVO_SMTP_PASS = os.getenv("MAIL_PASSWORD")
BREVO_SENDER_EMAIL = os.getenv("MAIL_FROM")
BREVO_SENDER_NAME = os.getenv("MAIL_NAME")
PUBLIC_SITE_URL = os.getenv("PUBLIC_SITE_URL")

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