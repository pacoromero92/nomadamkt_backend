from pathlib import Path
import smtplib
from email.message import EmailMessage
from jinja2 import Template

def send_emil_recovery_password (to:str,url,name:str):
    template_path = Path(__file__).parent.parent / "templates" / "send_email_recovery_password.html"

    html = template_path.read_text(encoding="utf-8")


    template = Template(html)

    html = template.render(
        name=name,
        url = url
    )

    message = EmailMessage()
    message["From"] = "soporte@nomadadigital.mx"
    message["To"] = to
    message["Subject"] = "Bienvenido  a Performance Nomada"

    message.set_content("Tu cliente de correo no soporta HTML.")

    message.add_alternative(html, subtype="html")

    with smtplib.SMTP_SSL("smtp.hostinger.com", 465) as smtp:
        smtp.login(
            "soporte@nomadadigital.mx",
            "n5^9n5V!v"
        )

        smtp.send_message(message)