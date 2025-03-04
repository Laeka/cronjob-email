import os
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import itertools
import http.server
import socketserver

load_dotenv()


def send_email(sender, recipients, subject, body, smtp_server, port, user, password):
    # Configure the message
    message = MIMEMultipart()
    message["From"] = sender
    message["To"] = ", ".join(
        recipients
    )  # Join recipients into a comma-separated string
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Send the email
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls()
            server.login(user, password)
            server.sendmail(sender, recipients, message.as_string())
        print(f"Email sent successfully from {sender} to {', '.join(recipients)}")
    except Exception as e:
        print(f"Failed to send email from {sender}: {e}")


EMAIL_PORT = 587

# List of email configurations
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

# List of recipients
recipients = [
    "contacto@kobsa.com.pe",
    "archivos@kobsa.com.pe",
    "abarrionuevo@kobsa.com.pe",
    "avera@kobsa.com.pe",
    "gestion.personal@kobsa.com.pe",
]

# Email data to send
subject = "Pago de mi liquidacion atrasado 1 año y 6 meses"
body = (
    "Por favor pagar lo restante de mi liquidacion mi dni es: 72767027. "
    "Se los suplico lo necesito urgente, mi numero de cuenta bbva es: 0011-0814-0260747032 - "
    "mi numero de celular es: 947307539"
)


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Server is running")


port = int(os.environ.get("PORT", 10000))
with socketserver.TCPServer(("", port), Handler) as httpd:
    print(f"Serving on port {port}")
    import threading

    server_thread = threading.Thread(target=httpd.serve_forever)
    server_thread.daemon = True
    server_thread.start()

    # Rotate between email accounts
    for config in itertools.cycle(email_configurations):
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
        # Wait 5 minutes before sending the next email
        time.sleep(300)
