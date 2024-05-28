from pathlib import Path

from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr

from cor_auth.conf.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_FROM_NAME="COR-Identity",
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent.parent / "templates",
)

async def send_email_code(email: EmailStr, host: str, verification_code):
    """
    The send_email function sends an email to the user with a link to confirm their email address.
        Args:
            email (str): The user's email address.
            host (str): The hostname that will be used in constructing a URL for confirming their account registration.

    :param email: EmailStr: Validate the email address
    :param host: str: Pass the hostname of the server to the template
    :return: A coroutine object
    """
    print("sending email...")
    try:
        message = MessageSchema(
            subject="Confirm your email ",
            recipients=[email],
            template_body={
                "host": host,
                "code": verification_code,
            },
            subtype=MessageType.html,
        )

        fm = FastMail(conf)
        await fm.send_message(message, template_name="email_templates.html")
        print("sending email done")
    except ConnectionErrors as err:
        print(err)
