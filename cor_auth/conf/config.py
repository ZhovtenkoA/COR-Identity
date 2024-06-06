from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    sqlalchemy_database_url: str = "sqlite:///./sql_auth.db"
    algorithm: str = "ALGORITHM"
    mail_username: str = "MAIL_USERNAME"
    mail_password: str = "MAIL_PASSWORD"
    mail_from: str = "Cor.Auth@EXAMPLE.COM"
    mail_port: int = 0
    mail_server: str = "MAIL_SERVER"
    pythonpath: str = "PYTHONPATH"
    encryption_key: str = "ENCRYPTION_KEY"
    private_key_path: str = "PYTHONPATH"
    public_key_path: str = "PYTHONPATH"

    def get_private_key(self):
        with open(self.private_key_path, 'rb') as f:
            private_key = f.read()
            return private_key

    def get_public_key(self):
        with open(self.public_key_path, 'rb') as f:
                public_key = f.read()
        return public_key

    class Config:
        env_file = "env.env"
        env_file_encoding = "utf-8"


settings = Settings()
private_key = settings.get_private_key()
public_key = settings.get_public_key()
