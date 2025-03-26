import os
import logging
import signal
import sys
import smtplib
import random
import datetime

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv


def send_email(sender, recipients, subject, body, smtp_server, port, user, password):
    logging.info(f"Attempting to send email from {sender} to {', '.join(recipients)}")
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = ", ".join(recipients)
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(user, password)
            server.sendmail(sender, recipients, message.as_string())
        logging.info(
            f"Email sent successfully from {sender} to {', '.join(recipients)}"
        )
    except Exception as e:
        logging.error(f"Failed to send email from {sender}: {e}")


def signal_handler(sig, frame):
    logging.info("Received interrupt signal, closing the application...")
    sys.exit(0)


def main():
    # Configurar manejadores de signal par una terminacion controlada
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    # Configurar el logger y cargar las variables de entorno
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )
    load_dotenv()
    logging.info("Variables de entorno cargadas exitosamente")
    logging.info("Inicio de ejecucion:" + datetime.datetime.now().isoformat())

    EMAIL_PORT = 587

    email_configurations = [
        {
            "smtp_server": "smtp.gmail.com",
            "port": EMAIL_PORT,
            "user": os.getenv("EMAIL_USER_1"),
            "password": os.getenv("EMAIL_PASSWORD_1"),
        },
        {
            "smtp_server": "smtp.gmail.com",
            "port": EMAIL_PORT,
            "user": os.getenv("EMAIL_USER_2"),
            "password": os.getenv("EMAIL_PASSWORD_2"),
        },
        {
            "smtp_server": "smtp.gmail.com",
            "port": EMAIL_PORT,
            "user": os.getenv("EMAIL_USER_3"),
            "password": os.getenv("EMAIL_PASSWORD_3"),
        },
        {
            "smtp_server": "smtp.gmail.com",
            "port": EMAIL_PORT,
            "user": os.getenv("EMAIL_USER_4"),
            "password": os.getenv("EMAIL_PASSWORD_4"),
        },
        {
            "smtp_server": "smtp.gmail.com",
            "port": EMAIL_PORT,
            "user": os.getenv("EMAIL_USER_5"),
            "password": os.getenv("EMAIL_PASSWORD_5"),
        },
    ]

    recipients = [
        "contacto@kobsa.com.pe",
        "archivos@kobsa.com.pe",
        "abarrionuevo@kobsa.com.pe",
        "avera@kobsa.com.pe",
        "gestion.personal@kobsa.com.pe",
        "sedanet@sedapal.com.pe",
    ]

    subject = "Exigencia de pago inmediato de liquidación pendiente (más de 1 año y 6 meses de retraso)"

    body = (
        "Estimados representantes de Kobsa y Sedapal:\n\n"
        "Por este medio, exijo formalmente el pago inmediato de mi liquidación pendiente, "
        "la cual ha sido injustamente retrasada por más de 1 año y 6 meses. "
        "A pesar de mis reiteradas gestiones (incluyendo contactos vía WhatsApp), "
        "no he recibido respuesta ni solución alguna.\n\n"
        "Mis datos para agilizar el proceso:\n"
        "- DNI: 72767027\n"
        "- Número de celular: 947307539\n"
        "- Cuenta BBVA: 0011-0814-0260747032\n\n"
        "Requiero que este pago se concrete el mismo día de recepción de este mensaje. "
        "De no recibir confirmación, procederé a escalar este reclamo ante las autoridades de Sedapal.\n\n"
        "Atentamente,\n"
        "Cristian Tocto"
    )

    config = random.choice(email_configurations)
    send_email(
        sender=config["user"],
        recipients=recipients,
        subject=subject,
        body=body,
        smtp_server=config["smtp_server"],
        port=config["port"],
        user=config["user"],
        password=config["password"],
    )


if __name__ == "__main__":
    main()
