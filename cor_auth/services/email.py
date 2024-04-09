from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from cor_auth.conf.config import settings
from cor_auth.services.auth import auth_service

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="John Snow",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
)


async def send_email(email: EmailStr, username: str, host: str):
    """
    The send_email function sends an email to the user with a link to confirm their email address.
        Args:
            email (str): The user's email address.
            username (str): The username of the user who is registering for an account.  This will be used in the message body of the confirmation message sent to them via FastMail.
            host (str): The hostname that will be used in constructing a URL for confirming their account registration.

    :param email: EmailStr: Validate the email address
    :param username: str: Pass the username to the template
    :param host: str: Pass the hostname of the server to the template
    :return: A coroutine object
    """
    try:
        token_verification = auth_service.create_email_token({"sub": email})
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={
                "host": host,
                "username": username,
                "token": token_verification,
            },
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_templates.html")
    except ConnectionErrors as err:
        print(err)