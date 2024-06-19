import os
import urllib
from pathlib import Path

from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


class Settings(BaseSettings):
    api_url: str
    api_host: str
    api_token: str
    db_connection_string: str

    class Config:
        # Load the .env file located in the project's root directory
        env_file = Path(__file__).resolve().parent.parent / ".env"


def get_settings() -> Settings:
    # Sprawdź, czy istnieje plik .env
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if env_path.exists():
        # Jeśli plik .env istnieje, użyj go do wczytania ustawień
        settings = Settings(_env_file=env_path, _env_file_encoding='utf-8')
    else:
        # Jeśli plik .env nie istnieje, wczytaj z zmiennej środowiskowej
        settings = Settings(
            api_url=os.getenv("API_URL"),
            api_host=os.getenv("API_HOST"),
            api_token=os.getenv("API_TOKEN"),
            db_connection_string=os.getenv("DB_CONNECTION_STRING")
        )

    return settings


params = urllib.parse.quote_plus(get_settings().db_connection_string)

# Create the SQLAlchemy engine
engine = create_engine(f'mssql+pyodbc:///?odbc_connect={params}')


def get_db():
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)


