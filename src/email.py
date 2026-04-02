import os
import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv

from src.global_variables import CALENDAR_URL

load_dotenv()

def send_email(changes: list[str]):
    """
    Send an email with the given changes.
    Args:
        changes (dict[str, list[str]]): A dictionary with lists of added and removed entries.
    """

    smtp_host = os.environ["SMTP_HOST"]
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ["SMTP_USER"]
    smtp_pass = os.environ["SMTP_PASS"]
    email_to = os.environ["EMAIL_TO"]
    email_from = os.environ.get("EMAIL_FROM", smtp_user)

    msg = EmailMessage()
    msg["Subject"] = "ListadoManga: release date changes detected"
    msg["From"] = email_from
    msg["To"] = email_to
    content_parts = []
    
    if changes["entries_added"]:
        content_parts.append(
            "The following new volumes were detected in the Listado Manga calendar:\n"
            + "\n".join(changes["entries_added"])
            + "\n"
        )
    
    if changes["entries_removed"]:
        content_parts.append(
            "The following volumes were removed from the Listado Manga calendar:\n"
            + "\n".join(changes["entries_removed"])
            + "\n"
        )
    
    content_parts.append(f"Source: {CALENDAR_URL}")
    
    msg.set_content("\n".join(content_parts))

    #print(msg)

    with smtplib.SMTP(smtp_host, smtp_port) as s:
        s.starttls()
        s.login(smtp_user, smtp_pass)
        s.send_message(msg)