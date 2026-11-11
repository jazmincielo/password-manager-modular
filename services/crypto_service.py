import secrets
import string
from cryptography.fernet import Fernet
from config.settings import settings

class CryptoService:
    def __init__(self):
        # Inicializar el cifrador con la clave configurada en settings
        key = settings.SECRET_KEY.encode() if settings.SECRET_KEY else Fernet.generate_key()
        self.cipher = Fernet(key)

    def encrypt(self, plain_text: str) -> str:
        """Cifra una contraseña en texto plano usando Fernet (AES)."""
        return self.cipher.encrypt(plain_text.encode()).decode()

    def decrypt(self, cipher_text: str) -> str:
        """Descifra el hash encriptado."""
        try:
            return self.cipher.decrypt(cipher_text.encode()).decode()
        except Exception:
            return "Error al descifrar (Clave Inválida)"

    @staticmethod
    def generate_random_password(length: int = 16) -> str:
        """Genera una contraseña aleatoria y segura."""
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
        return ''.join(secrets.choice(alphabet) for _ in range(length))

crypto_service = CryptoService()
