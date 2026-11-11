import os
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    PORT: int = int(os.getenv("PORT", 8080))
    TITLE: str = "Secure Vault - Gestor de Contraseñas (Modular)"

    @classmethod
    def validate(cls):
        if not cls.DATABASE_URL:
            raise ValueError("ERROR: La variable DATABASE_URL no está configurada en el archivo .env")
        if not cls.SECRET_KEY:
            raise ValueError("ERROR: La variable SECRET_KEY no está configurada en el archivo .env")

settings = Settings()
