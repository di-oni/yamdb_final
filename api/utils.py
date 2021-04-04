import logging
import uuid
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMessage

from rest_framework_simplejwt.tokens import RefreshToken

logging.basicConfig(
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("debug.log"),
        logging.StreamHandler()
    ]
)


def send_message(email, generated_code):
    """Send a message to email with generated code."""
    mail = EmailMessage(
        'Confirm your email',
        generated_code,
        settings.EMAIL_HOST_USER,
        [email, ]
    )

    try:
        mail.send()
        result = f'message was sended to {email} with confirmation code.'
        return result
    except SMTPException as e:
        logging.exception("Exception occurred", e)


def generate_code():
    """Generate a random code."""
    code = uuid.uuid4().hex
    return code


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
