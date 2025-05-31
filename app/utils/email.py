import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

def enviar_alerta_consumo(nombre_cliente: str, fecha: str, consumo: float):
    if not all([EMAIL_HOST, EMAIL_USER, EMAIL_PASS, EMAIL_TO]):
        print("Configuración de correo incompleta.")
        return

    mensaje = f"⚠️ Alerta de Consumo

Cliente: {nombre_cliente}
Fecha: {fecha}
Consumo: {consumo} m³"
    msg = MIMEText(mensaje)
    msg["Subject"] = "Alerta de Consumo Elevado"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_TO

    try:
        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_USER, EMAIL_PASS)
            server.sendmail(EMAIL_USER, EMAIL_TO, msg.as_string())
        print("Correo enviado correctamente.")
    except Exception as e:
        print("Error al enviar correo:", e)