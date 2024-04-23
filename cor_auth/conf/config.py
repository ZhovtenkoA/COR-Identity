from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = "sqlite:///./sql_auth.db"
    secret_key: str = "SECRET_KEY"
    algorithm: str = "ALGORITHM"
    mail_username: str = "MAIL_USERNAME"
    mail_password: str = "MAIL_PASSWORD"
    mail_from: str = "JOHN.SNOW@EXAMPLE.COM"
    mail_port: int = 0
    mail_server: str = "MAIL_SERVER"
    redis_host: str = "REDIS_HOST"
    redis_port: int = 0
    pythonpath: str = "PYTHONPATH"
    encryption_key: str = "ENCRYPTION_KEY"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
