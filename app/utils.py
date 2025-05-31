
import smtplib
from email.message import EmailMessage

def enviar_email(destinatario: str, asunto: str, contenido: str):
    remitente = "tucorreo@example.com"
    contraseña = "tu-contraseña-app"

    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario
    msg.set_content(contenido)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(remitente, contraseña)
        smtp.send_message(msg)
