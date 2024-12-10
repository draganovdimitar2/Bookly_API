from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from src.config import Config
import logging

def create_message(recipients: list[str], subject: str, body: str):
    message = Mail(
        from_email=(Config.MAIL_FROM, Config.MAIL_FROM_NAME),
        to_emails=recipients,
        subject=subject,
        html_content=body
    )
    return message

async def send_email(recipients: list[str], subject: str, body: str):
    message = create_message(recipients, subject, body)
    try:
        sg = SendGridAPIClient(Config.SENDGRID_API_KEY)
        response = sg.send(message)
        logging.info(f"Email sent successfully: {response.status_code}")
    except Exception as e:
        logging.error(f"Failed to send email: {e}")
        raise e  # Re-raise the exception to capture it in the logs