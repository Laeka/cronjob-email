import os
import logging
import signal
import sys
import smtplib
import random

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
    ]

    subject = "Pago de mi liquidacion atrasado 1 año y 6 meses"
    body = (
        "Por favor pagar lo restante de mi liquidacion mi dni es: 72767027. "
        "Se los suplico lo necesito urgente, mi numero de cuenta bbva es: 0011-0814-0260747032 - "
        "Sigo sin tener respuesta y por whatsapp ya no me contestan ya pasaron: 1 año y 3 meses por favor!!"
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
