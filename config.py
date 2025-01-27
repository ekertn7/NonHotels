"""Settings"""

from typing import Optional
from datetime import timedelta

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgresql_driver: str
    postgresql_host: str
    postgresql_port: int
    postgresql_user: str
    postgresql_pass: str
    postgresql_name: str

    token_name: str
    token_lifetime_minutes: int
    token_secret: str
    token_algorithm: str

    @property
    def postgresql_url(self) -> str:
        return (
            f'{self.postgresql_driver}://{self.postgresql_user}:'
            f'{self.postgresql_pass}@{self.postgresql_host}:'
            f'{self.postgresql_port}/{self.postgresql_name}')

    @property
    def token_lifetime(self) -> str:
        return timedelta(minutes=self.token_lifetime_minutes)

    class Config:
        env_file = '.env'


settings = Settings()
