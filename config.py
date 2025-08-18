import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "lovelove#secret$key$2024")
    
    # Configuração do banco de dados
    USER = os.getenv("DB_USER", "postgres")
    PASSWORD = os.getenv("DB_PASSWORD", "paiva123")
    HOST = os.getenv("DB_HOST", "localhost")
    PORT = os.getenv("DB_PORT", "5432")
    DATABASE = os.getenv("DB_NAME", "lovelove")

    # Verifica se é PostgreSQL (Render) ou SQLite (local)
    if os.getenv("RENDER"):
        # PostgreSQL para Render
        SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    else:
        # PostgreSQL para desenvolvimento local
        SQLALCHEMY_DATABASE_URI = os.getenv(
            "DATABASE_URL",
            f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"
        )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "lovelove.jwt.secret.2024")
